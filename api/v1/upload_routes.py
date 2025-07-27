import json
import time
import traceback
from contextlib import asynccontextmanager
from datetime import datetime
from io import BytesIO
from typing import Annotated

import cv2
import numpy as np
import uvicorn
from fastapi import APIRouter, Form, Header, HTTPException, UploadFile
from fastapi.responses import FileResponse, StreamingResponse, UJSONResponse
from fastapi_utils.timing import add_timing_middleware
import logging


route = APIRouter()

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


@route.post('/api/v1/upload/text', response_class=UJSONResponse)
async def upload_text(
    text: str = Form(...),
    request_id: Annotated[str, Header()] = None
):
    """
    Upload a text file.
    """
    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty.")
    
    # Process the text here (e.g., save it, analyze it, etc.)
    try:
        logging.info(f"Received text: {text[:100]}...")  # Log first 100 characters for brevity

    except Exception as e:
        logging.error(f"Error processing text: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Error processing text.")
    
    return UJSONResponse(content={"message": "Text uploaded successfully", "length": len(text)})


@route.post('/api/v1/upload/pdf', response_class=UJSONResponse)
async def upload_pdf(
    file: UploadFile = Form(),
    request_id: Annotated[str, Header()] = None
):
    """
    Upload a PDF file.
    """
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF.")
    
    if len(file) == 0:
        logging.error("File is empty.")
        raise HTTPException(status_code=400, detail="File is empty.")

    # Process the PDF file here (e.g., save it, extract text, etc.)
    try:
        content = await file.read()
        logging.info(f"Received PDF file: {file.filename}, size: {len(content)} bytes")


    except Exception as e:
        logging.error(f"Error processing file: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Error processing file.")
    
    return UJSONResponse(content={"message": "PDF uploaded successfully", "filename": file.filename})

@route.post('/api/v1/upload/image', response_class=UJSONResponse)
async def upload_image(
    file: UploadFile = Form(),
    request_id: Annotated[str, Header()] = None
):
    """
    Upload an image file.
    """
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        raise HTTPException(status_code=400, detail="File must be an image (PNG, JPG, JPEG, GIF).")
    
    if len(file) == 0:
        logging.error("File is empty.")
        raise HTTPException(status_code=400, detail="File is empty.")

    # Process the image file here (e.g., save it, analyze it, etc.)
    try:
        content = await file.read()
        logging.info(f"Received image file: {file.filename}, size: {len(content)} bytes")

    except Exception as e:
        logging.error(f"Error processing file: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Error processing file.")
    
    return UJSONResponse(content={"message": "Image uploaded successfully", "filename": file.filename})