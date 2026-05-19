import streamlit as st


def render_history_download():

    if st.session_state.get("messages"):

        st.markdown("---")

        st.markdown("## 📥 Export Conversation")

        chat_text = "\n\n".join(
            [
                f"{m['role'].upper()}: {m['content']}"
                for m in st.session_state.messages
            ]
        )

        st.download_button(
            label="⬇ Download Chat History",
            data=chat_text,
            file_name="medical_chat_history.txt",
            mime="text/plain",
            use_container_width=True
        )