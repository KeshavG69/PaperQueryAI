import streamlit as st
from helper import ask, llm_call, greet_chain, llm_respond
from icecream import ic 


ic.disable()

st.set_page_config(page_title="PaperQueryAI", page_icon="🤖", layout="wide")

st.title("PaperQueryAI: Chatbot Based On Research Papers")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        # Display references in an expandable container
        if (
            message["role"] == "assistant"
            and "references" in message
            and message["references"]
        ):
            with st.expander("🔗 View References", expanded=False):
                for paper_name, paper_link in message["references"].items():
                    st.markdown(f"- [{paper_name}]({paper_link})")

# User input
if prompt := st.chat_input("Ask your question based on research papers:"):

    # Append user input to session state and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant response
    with st.chat_message("assistant"):
        with st.spinner("Processing your query..."):
            greet_score = greet_chain.invoke({"user_query": prompt})

            if greet_score.binary_score == "yes":
                # print something to know that it is a greeting query
                ic("This is a greeting query")
                response = st.write_stream(llm_respond(prompt))

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": response,
                    }
                )
            else:
                # print something to know that it is a research query
                ic("This is a research query")
                ref, jina_text, pdf_text = ask(prompt)

                response = st.write_stream(llm_call(prompt, jina_text, pdf_text))

                # Display references in an expandable container
                if ref:
                    with st.expander("🔗 View References", expanded=False):
                        for paper_name, paper_link in ref.items():
                            st.markdown(f"- [{paper_name}]({paper_link})")

    # Append assistant response to session state
                st.session_state.messages.append(
                    {"role": "assistant", "content": response, "references": ref}
                )
