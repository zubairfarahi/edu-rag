import json
import time
import traceback
from contextlib import asynccontextmanager
from datetime import datetime
from io import BytesIO
from typing import Annotated

import numpy as np
import uvicorn
from fastapi import APIRouter, Form, Header, HTTPException, UploadFile
from fastapi.responses import FileResponse, StreamingResponse, UJSONResponse
from fastapi_utils.timing import add_timing_middleware
import logging
import os
import tempfile

from services.text_utils import TextFileLoader, CharacterTextSplitter
from services.pdf_utils import PDFLoader
from services.vectordatabase import VectorDatabase
from services.chatmodel import ChatOpenAI
from services.prompts import SystemRolePrompt, UserRolePrompt

route = APIRouter()



text_splitter = CharacterTextSplitter()

system_template = """Use the following context to answer a users question. If you cannot find the answer in the context, say you don't know."""
system_role_prompt = SystemRolePrompt(system_template)

user_prompt_template = """Context:\n{context}\n\nQuestion:\n{question}"""
user_role_prompt = UserRolePrompt(user_prompt_template)

# Store user vector DB in memory (in prod use Redis or DB)
user_db_store = {}


@route.get('/ping')
async def ping():
    
    time_n = datetime.fromtimestamp(time.time())
    time_now = time_n.strftime("%Y-%m-%dT%H:%M:%S+02:00")
    
    server_info = {
        "message": "ping test",
        "applicationName": "Edu Chat RAG API",
        "version": "v0.1.0",
        "serverTime": time_now
    }
    
    return server_info



@route.post("/api/v1/upload/pdf", response_class=UJSONResponse)
async def upload_pdf(file: UploadFile, user_id: str = Header(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files allowed.")

    try:
        suffix = ".pdf"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_path = temp_file.name
            content = await file.read()
            temp_file.write(content)

        loader = PDFLoader(temp_path)
        documents = loader.load_documents()
        texts = text_splitter.split_texts(documents)

        vector_db = VectorDatabase()
        vector_db = await vector_db.abuild_from_list(texts)

        # store vector DB temporarily using user_id
        user_db_store[user_id] = vector_db

        return {"message": "PDF processed and indexed", "chunks": len(texts)}

    except Exception as e:
        logging.error(f"PDF upload error: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Failed to process PDF.")
    finally:
        try:
            os.remove(temp_path)
        except Exception as e:
            logging.warning(f"Temp file deletion failed: {e}")


@route.post("/api/v1/ask", response_class=UJSONResponse)
async def ask_question(
    question: str = Form(...),
    user_id: str = Header(...)
):
    if user_id not in user_db_store:
        raise HTTPException(status_code=400, detail="No vector DB found for this user. Please upload a document first.")

    try:
        vector_db = user_db_store[user_id]
        chat_openai = ChatOpenAI()

        context_list = vector_db.search_by_text(question, k=4)
        context_prompt = "\n".join([c[0] for c in context_list])

        formatted_system_prompt = system_role_prompt.create_message()
        formatted_user_prompt = user_role_prompt.create_message(question=question, context=context_prompt)

        response_text = ""
        async for chunk in chat_openai.astream([formatted_system_prompt, formatted_user_prompt]):
            response_text += chunk
        # return {"answer": response_text, "context_used": context_list}
        return {"answer": response_text}

    except Exception as e:
        logging.error(f"Question error: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Failed to process question.")
