import streamlit as st
from utils.api import ask_question


def render_chat():

    st.markdown("## 💬 Chat with MediBot")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Render chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input(
        "Ask medical questions from uploaded documents..."
    )

    if user_input:

        # USER MESSAGE
        with st.chat_message("user"):
            st.markdown(user_input)

        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        # ASSISTANT RESPONSE
        with st.chat_message("assistant"):

            with st.spinner("Analyzing medical documents..."):

                response = ask_question(user_input)

                if response.status_code == 200:

                    data = response.json()
                    answer = data["response"]

                    st.markdown(answer)

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": answer
                        }
                    )

                else:
                    st.error(f"Error: {response.text}")