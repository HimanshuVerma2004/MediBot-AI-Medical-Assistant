import streamlit as st
from utils.api import upload_pdfs_api


def render_uploader():

    st.sidebar.markdown("# 📂 Document Center")

    st.sidebar.info(
        "Upload medical PDFs and chat with your AI medical assistant."
    )

    uploaded_files = st.sidebar.file_uploader(
        "Upload Medical PDFs",
        type="pdf",
        accept_multiple_files=True
    )

    if uploaded_files:

        st.sidebar.success(
            f"{len(uploaded_files)} file(s) selected"
        )

    if st.sidebar.button(
        "🚀 Upload to Database",
        use_container_width=True
    ):

        if not uploaded_files:
            st.sidebar.warning("Please upload at least one PDF")
            return

        with st.sidebar:

            with st.spinner(
                "Processing and embedding documents..."
            ):

                response = upload_pdfs_api(uploaded_files)

                if response.status_code == 200:
                    st.sidebar.success(
                        "✅ Documents uploaded successfully"
                    )
                else:
                    st.sidebar.error(
                        f"❌ Error: {response.text}"
                    )