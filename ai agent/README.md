# ai-agent-for-PDFs-email-json-files


This is an AI-based file processing system using FastAPI that can intelligently classify and handle files in PDF, JSON, or Email format. It detects the type and intent of the uploaded file, processes it with appropriate agents, and provides a detailed output.

---

## Features

- Upload files via a responsive web UI
- Auto-detects file type (`email`, `json`, `pdf`)
- Context-aware agents extract structured data:
  - Email Agent: Parses "From", "To", "Subject", and Body
  - JSON Agent: Validates and parses JSON fields
  - PDF Agent: Extracts text and flags compliance issues
- Intent detection and routing of actions
- Memory module to store logs of processed files
- Dark/light theme toggle for frontend
---

##  Tech Stack

- **Backend**: FastAPI, Python
- **Frontend**: HTML, CSS (Bootstrap), JS
- **PDF Parsing**: PyMuPDF (`fitz`)
- **Email Parsing**: Python `email` module
- **JSON Validation**: `json` and `jsonschema`
- **Cross-Origin**: CORS middleware enabled for API access
---
### Landing page
![image](https://github.com/user-attachments/assets/19866231-5efc-41c7-998d-9701fedd121f)
---
### Sample inputs
![image](https://github.com/user-attachments/assets/b02a01cf-f455-46a2-9afc-7792e550de0b)
---
### Sample output
![image](https://github.com/user-attachments/assets/dc54f007-9d0a-4f42-8fc3-8f4dcfd642c8)
![image](https://github.com/user-attachments/assets/463f48d8-fbbb-42ed-af25-13ca01acee19)


