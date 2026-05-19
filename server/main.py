from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).parent / ".env")

import os

print("=== DEBUG KEY ===", repr(os.getenv("GOOGLE_API_KEY")))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.upload_pdfs import router as upload_router
from routes.ask_question import router as ask_router

app = FastAPI(
    title="Medical Assistant API",
    description="API for AI Medical Assistant Chatbot"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)
app.include_router(ask_router)

print("ROUTES REGISTERED:")
for route in app.routes:
    print(route.path)