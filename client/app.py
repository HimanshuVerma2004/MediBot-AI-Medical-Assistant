import streamlit as st
from components.upload import render_uploader
from components.history_download import render_history_download
from components.chatUI import render_chat

st.set_page_config(
    page_title="MediBot AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- CUSTOM CSS ----------
st.markdown(
    """
    <style>

    .stApp {
        background: linear-gradient(to bottom right, #f8fbff, #eef4ff);
    }

    .main-title {
        font-size: 3rem;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 0.3rem;
    }

    .subtitle {
        color: #475569;
        font-size: 1.05rem;
        margin-bottom: 2rem;
    }

    .glass-card {
        background: rgba(255,255,255,0.75);
        backdrop-filter: blur(12px);
        border-radius: 20px;
        padding: 1.2rem;
        border: 1px solid rgba(255,255,255,0.4);
        box-shadow: 0 8px 30px rgba(0,0,0,0.06);
    }

    .stChatMessage {
        border-radius: 18px;
        padding: 12px;
        margin-bottom: 10px;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(to bottom, #0f172a, #1e293b);
        color: white;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p {
        color: white !important;
    }

    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        text-align: center;
    }

    .metric-title {
        font-size: 0.9rem;
        color: #64748b;
    }

    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: #2563eb;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ---------- HEADER ----------
st.markdown(
    """
    <div class='glass-card'>
        <div class='main-title'>🩺 MediBot AI</div>
        <div class='subtitle'>
            AI-powered Medical Document Assistant using RAG + Pinecone + Groq
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------- DASHBOARD METRICS ----------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class='metric-card'>
            <div class='metric-title'>AI Model</div>
            <div class='metric-value'>Groq</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class='metric-card'>
            <div class='metric-title'>Vector Database</div>
            <div class='metric-value'>Pinecone</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div class='metric-card'>
            <div class='metric-title'>Embeddings</div>
            <div class='metric-value'>Gemini</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)

# ---------- MAIN COMPONENTS ----------
render_uploader()
render_chat()
render_history_download()