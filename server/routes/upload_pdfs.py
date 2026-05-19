from fastapi import APIRouter, UploadFile, File
from typing import List
from modules.load_vectorstore import load_vectorstore
from fastapi.responses import JSONResponse
from logger import logger

router = APIRouter()

@router.post("/upload_pdfs/")
async def upload_pdfs(
    files: List[UploadFile] = File(...)
):

    print("UPLOAD ENDPOINT HIT")

    try:

        logger.info("Received uploaded files")

        load_vectorstore(files)

        logger.info("Document added to vectorstore")

        return {
            "message": "Files processed and vectorstore updated"
        }

    except Exception as e:

        print("ACTUAL ERROR:")
        print(type(e))
        print(e)

        logger.exception("Error during PDF upload")

        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )