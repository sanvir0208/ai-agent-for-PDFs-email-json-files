import os
import shutil
from typing import Dict
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from backend.agents import classifier, email_agent, json_agent, pdf_agent
from backend.memory import memory
from backend.router import action_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "../frontend")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)) -> Dict:
    filename = file.filename or "untitled"
    file_location = os.path.join(UPLOAD_FOLDER, filename)

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    content_type = file.content_type or ""
    content = ""

    if content_type.startswith("text") or filename.endswith((".json", ".txt", ".eml")):
        file.file.seek(0)
        content = (await file.read()).decode("utf-8", errors="ignore")

    file_format, intent = classifier.detect_format_and_intent(filename, content)

    agent_output = {
        "format": file_format,
        "intent": intent,
        "filename": filename,
    }

    if file_format == "email":
        agent_output["email_data"] = email_agent.extract_email_fields(content)
    elif file_format == "json":
        agent_output["json_data"] = json_agent.validate_json_schema(content)
    elif file_format == "pdf":
        agent_output["pdf_data"] = pdf_agent.extract_pdf_fields(file_location)
    else:
        agent_output["message"] = "Unsupported file format"

    memory.log(agent_output)
    agent_output["action"] = action_router(agent_output)

    return agent_output
