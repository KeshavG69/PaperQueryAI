import requests
from langchain_core.output_parsers import StrOutputParser
import os
import hashlib
from dotenv import load_dotenv
import urllib
from langchain_core.prompts import ChatPromptTemplate
import uuid
import streamlit as st
import shutil
from langchain_core.documents import Document
from langchain_community.document_loaders import DirectoryLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from templates import template
from serpapi import GoogleSearch


load_dotenv() 

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",temperature=0.1,api_key=st.secrets['GOOGLE_API_KEY'])


query_cache = {}
pdf_cache_file = "pdf_files/cache.txt"

def hash_link(link):
    """Generate a unique hash for a given link."""
    return hashlib.md5(link.encode('utf-8')).hexdigest()

def load_pdf_cache():
  
  """Load cached PDF links and their hashed filenames."""
  cache = {}
  if os.path.exists(pdf_cache_file):
      with open(pdf_cache_file, 'r') as f:
          for line in f:
              hash_val, filename = line.strip().split(',', 1)
              cache[hash_val] = filename
  return cache

def save_pdf_cache(cache):
  """Save updated cache to a file."""

  with open(pdf_cache_file, 'w') as f:
      for hash_val, filename in cache.items():
          f.write(f"{hash_val},{filename}\n")

def get_research_papers(query,num:int=15):
  
  params = {
  "engine": "google_scholar",
  "q": query,
  "api_key": st.secrets['SERPAPI_KEY'],
  "num":num
  }

  search = GoogleSearch(params)
  results = search.get_dict()
  organic_results = results["organic_results"]


  links=[]
  ref={}

  for result in organic_results:
    try:
      links.append(result['link'])
      
      ref[result['title']]=result['link']
      
      
    except:
      pass
  return links,ref



def categorise_links(links):

  jina_links=[]
  pdf_links=[]
  for link in links:
    if 'https://books.google.com/' not in link:
      response = requests.head(link, allow_redirects=True)
      content_type = response.headers.get('Content-Type', '').lower()
      if 'application/pdf' in content_type :
        pdf_links.append(link)
      else:
        jina_links.append('https://r.jina.ai/'+link)
  return jina_links,pdf_links


def download_pdf_files(pdf_links, directory='pdf_files'):
  """Download PDF files if not already cached."""
  if not os.path.exists(directory):
      os.makedirs(directory)

  cache = load_pdf_cache()
  for link in pdf_links:
      hash_val = hash_link(link)
      if hash_val not in cache:
          filename = f"{uuid.uuid4()}.pdf"
          filepath = os.path.join(directory, filename)
          try:
              urllib.request.urlretrieve(link, filepath)
              cache[hash_val] = filename
          except Exception as e:
              print(f"Failed to download {link}: {e}")
  save_pdf_cache(cache)



def jina_text_read(jina_links):
  jina_text=[]
  for link in jina_links:
    response = requests.get(link)
    text = response.text
    document=Document(page_content=text,metadata={'source':link})
    jina_text.append(document)
  return jina_text

def pdf_text_read(directory='pdf_files'):
  loader = DirectoryLoader(directory, glob="**/*.pdf")
  pdf_text = loader.load()
  return pdf_text


def chain(query,jina_text,pdf_text):
  prompt = ChatPromptTemplate.from_template(template)
  answer_chain=prompt|llm|StrOutputParser()
  answer=answer_chain.invoke({'user_query':query,'jina_text':jina_text,'pdf_text':pdf_text})
  return answer

def ask(query):
  links,ref=get_research_papers(query)
  jina_links,pdf_links=categorise_links(links)
  download_pdf_files(pdf_links,'pdf_files')
  jina_text=jina_text_read(jina_links)
  pdf_text=pdf_text_read('pdf_files')
  answer=chain(query,jina_text,pdf_text)
  return answer



