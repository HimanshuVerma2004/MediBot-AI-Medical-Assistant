import os
import time
from pathlib import Path
from dotenv import load_dotenv
from tqdm.auto import tqdm

from pinecone import Pinecone, ServerlessSpec

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

PINECONE_ENV = "us-east-1"
PINECONE_INDEX_NAME = "medicalindex"

UPLOAD_DIR = "./uploaded_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

print("GOOGLE_API_KEY =", GOOGLE_API_KEY)

pc = Pinecone(api_key=PINECONE_API_KEY)

existing_indexes = pc.list_indexes().names()

if PINECONE_INDEX_NAME not in existing_indexes:

    pc.create_index(
        name=PINECONE_INDEX_NAME,
        dimension=3072,
        metric="dotproduct",
        spec=ServerlessSpec(
            cloud="aws",
            region=PINECONE_ENV
        )
    )

    while not pc.describe_index(PINECONE_INDEX_NAME).status["ready"]:
        time.sleep(1)

index = pc.Index(PINECONE_INDEX_NAME)


def load_vectorstore(uploaded_files):

    embed_model = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=GOOGLE_API_KEY
    )

    file_paths = []

    for file in uploaded_files:

        save_path = Path(UPLOAD_DIR) / file.filename

        with open(save_path, "wb") as f:
            f.write(file.file.read())

        file_paths.append(str(save_path))

    for file_path in file_paths:

        print(f"Processing: {file_path}")

        loader = PyPDFLoader(file_path)
        documents = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )

        chunks = splitter.split_documents(documents)

        print("TOTAL CHUNKS =", len(chunks))

        cleaned_chunks = []

        for chunk in chunks:

            text = chunk.page_content.strip()

            if len(text) < 5:
                continue

            cleaned_chunks.append(chunk)

        print("VALID CHUNKS =", len(cleaned_chunks))

        embeddings_data = []

        for i, chunk in enumerate(cleaned_chunks):

            try:

                text = chunk.page_content.strip()

                embedding = embed_model.embed_query(text)
                metadata = chunk.metadata.copy()

                metadata["text"] = text

                embeddings_data.append(
                    (
                        f"{Path(file_path).stem}-{i}",
                        embedding,
                        chunk.metadata
                    )
                )

                print(f"Embedded chunk {i}")

            except Exception as e:

                print(f"FAILED CHUNK {i}")
                print(e)

        print("Uploading to Pinecone...")

        index.upsert(vectors=embeddings_data)

        print(f"Upload complete for {file_path}")