import streamlit as st
from helper import ask

# Streamlit title
st.title("Chatbot Based On Research Papers")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input for new queries
if prompt := st.chat_input("Ask your question based on research papers:"):
    # Add user's message to the chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response using the `ask` function
    with st.chat_message("assistant"):
        status_placeholder = st.empty()
        status_placeholder.markdown("_Processing your query..._")

        try:
            response = ask(prompt)
        except Exception as e:
            response = f"An error occurred: {e}"

        # Clear the status message and display the response
        status_placeholder.empty()
        st.markdown(response)

    # Save assistant's message in chat history
    st.session_state.messages.append({"role": "assistant", "content": response})