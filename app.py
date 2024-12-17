import streamlit as st
from helper import ask, llm_call

st.set_page_config(page_title="PaperQueryAI", page_icon="🤖", layout="wide")


st.title("PaperQueryAI: Chatbot Based On Research Papers")


if "messages" not in st.session_state:
    st.session_state["messages"] = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
     
        if message["role"] == "assistant" and "references" in message:
            st.markdown("**References:**")
            for paper_name, paper_link in message["references"].items():
                st.markdown(f"- [{paper_name}]({paper_link})")


if prompt := st.chat_input("Ask your question based on research papers:"):

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)


    with st.chat_message("assistant"):
        with st.spinner("Processing your query..."):
            ref,jina_text, pdf_text = ask(prompt)

            
            


            response=st.write_stream(llm_call(prompt, jina_text, pdf_text))


            if ref:
                st.markdown("**References:**")
                for paper_name, paper_link in ref.items():
                    st.markdown(f"- [{paper_name}]({paper_link})")


    st.session_state.messages.append({
        "role": "assistant", 
        "content": response, 
        "references": ref
    })
