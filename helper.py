import requests
from langchain_core.output_parsers import StrOutputParser
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from io import BytesIO
import pdfplumber

from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate

import streamlit as st

from langchain_core.documents import Document

from langchain_google_genai import ChatGoogleGenerativeAI
from templates import template
from serpapi import GoogleSearch


load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.1,
    api_key=st.secrets["GOOGLE_API_KEY"],
    stream=True,
)


def get_research_papers(query, num: int = 20):

    params = {
        "engine": "google_scholar",
        "q": query,
        "api_key": st.secrets["SERPAPI_KEY"],
        "num": num,
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    organic_results = results["organic_results"]

    links = []
    ref = {}

    for result in organic_results:
        try:
            links.append(result["link"])

            ref[result["title"]] = result["link"]

        except:
            pass

    return links, ref


def check_link(link):
    """Check if the link points to a PDF or categorize as Jina link."""
    try:
       
        if "https://books.google.com/" in link:
            pass

        response = requests.head(link, timeout=10, allow_redirects=True)
        content_type = response.headers.get("Content-Type", "").lower()
        if "application/pdf" in content_type:
            return "pdf", link
    except requests.RequestException:
        pass  

    return "jina", link


def categorise_links(links):
    """Categorize links into PDF links and Jina links using parallel requests."""
    jina_links = []
    pdf_links = []

    with ThreadPoolExecutor(
        max_workers=10
    ) as executor:  # 10 threads for parallel execution
        futures = {executor.submit(check_link, link): link for link in links}

        for future in as_completed(futures):
            result_type, link = future.result()
            if result_type == "pdf":
                pdf_links.append(link)
            elif result_type == "jina":
                jina_links.append("https://r.jina.ai/" + link)

    return jina_links, pdf_links


def fetch_link_content(link):
    """Fetch the content of a link and return a Document."""
    try:
        response = requests.get(link, timeout=5)  
        response.raise_for_status()  
        text = response.text
        return Document(page_content=text, metadata={"source": link})
    except requests.RequestException as e:
        pass
        return None  


def jina_text_read(jina_links):
    """Fetch text content from multiple links in parallel and return as Documents."""
    jina_text = []

    with ThreadPoolExecutor(max_workers=10) as executor:  # Adjust max_workers as needed
        futures = {
            executor.submit(fetch_link_content, link): link for link in jina_links
        }

        for future in as_completed(futures):
            document = future.result()
            if document is not None:  # Add only successfully fetched documents
                jina_text.append(document)

    return jina_text


# def jina_text_read(jina_links):
#     jina_text = []
#     for link in jina_links:
#         response = requests.get(link)
#         text = response.text
#         document = Document(page_content=text, metadata={"source": link})
#         jina_text.append(document)
#     print(jina_text)
#     return jina_text


def fetch_pdf_text(link):
    """Fetch a PDF from a URL, extract its text, and wrap it in a Document."""
    try:
        response = requests.get(link, timeout=10)  # Fetch PDF with a timeout
        if response.status_code != 200:

            return None

        pdf_file = BytesIO(response.content)
        text = ""
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                extracted_text = page.extract_text()
                if extracted_text:  # Avoid None results
                    text += extracted_text

        return Document(page_content=text, metadata={"source": link})
    except Exception as e:
        pass

        return None  # Gracefully skip any problematic links


def pdf_text_read(pdf_links):
    """Fetch and extract text from multiple PDFs concurrently."""
    pdf_text = []

    with ThreadPoolExecutor(
        max_workers=5
    ) as executor:  # Adjust max_workers for concurrency
        futures = {executor.submit(fetch_pdf_text, link): link for link in pdf_links}

        for future in as_completed(futures):
            document = future.result()
            if document is not None:  # Only add successful results
                pdf_text.append(document)

    return pdf_text


# def pdf_text_read(pdf_links):
#     pdf_text = []
#     for link in pdf_links:
#         response = requests.get(link)
#         if response.status_code == 200:
#             pdf_file = BytesIO(response.content)
#             text = ""
#             with pdfplumber.open(pdf_file) as pdf:
#                 for page in pdf.pages:
#                     text += page.extract_text()
#             pdf_text.append(Document(page_content=text, metadata={"source": link}))
#     print(pdf_text)
#     return pdf_text


# def chain(query, jina_text, pdf_text):


#     answer = answer_chain.invoke(
#         {"user_query": query, "jina_text": jina_text, "pdf_text": pdf_text}
#     )
#     return answer


def ask(query):
    links, ref = get_research_papers(query)
    jina_links, pdf_links = categorise_links(links)

    jina_text = jina_text_read(jina_links)
    pdf_text = pdf_text_read(pdf_links)

        
    return ref,jina_text, pdf_text

def llm_call(query, jina_text, pdf_text):
    prompt = ChatPromptTemplate.from_template(template)
    answer_chain = prompt | llm | StrOutputParser()
    for chunk in answer_chain.stream(
        {"user_query": query, "jina_text": jina_text, "pdf_text": pdf_text}
    ):
        yield chunk

def ask_without_streaming(query):
    links, ref = get_research_papers(query)
    jina_links, pdf_links = categorise_links(links)

    jina_text = jina_text_read(jina_links)
    pdf_text = pdf_text_read(pdf_links)
    prompt = ChatPromptTemplate.from_template(template)
    answer_chain = prompt | llm | StrOutputParser()
    answer = answer_chain.invoke(
        {"user_query": query, "jina_text": jina_text, "pdf_text": pdf_text}
    )
    return answer
