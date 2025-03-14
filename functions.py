# functions.py

import streamlit as st
import requests
import json
import re
from PyPDF2 import PdfReader
from docx import Document

# -------------------------
# Session State Helpers
# -------------------------
def store_in_state(key, value):
    st.session_state[key] = value

def get_from_session_state(key, default=None):
    return st.session_state.get(key, default)

def initialize_session_state():
    """
    Prepopulates certain fields so we avoid KeyErrors.
    """
    defaults = {
        "job_title": "",
        "company_name": "",
        "location": "",
        "company_website": "",
        "industry": "",
        "company_size": "",
        "founded_year": 0,
        "company_mission": "",
        "department": "",
        "team_size": 0,
        "direct_supervisor": "",
        "department_goals": "",
        "technologies_used": [],
        "travel_required": "",
        "remote_policy": "",
        "job_reason": "New Role",
        "responsibility_distribution": "",
        "tasks": "",
        "job_challenges": "",
        "recurring_tasks": "",
        "autonomy_level": "Low",
        "hard_skills": "",
        "soft_skills": "",
        "salary_range": "",
        "benefits": "",
        "health_benefits": "",
        "learning_opportunities": "",
        "interview_stages": 0,
        "uploaded_file": {},
        "input_url": "",
        "current_section": 0
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

# -------------------------
# File / Text Extraction
# -------------------------
def extract_text_from_pdf(file):
    reader = PdfReader(file)
    txt = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            txt.append(text)
    return {"job_description": " ".join(txt)}

def extract_text_from_docx(file):
    doc = Document(file)
    content = []
    for para in doc.paragraphs:
        content.append(para.text)
    return {"job_description": "\n".join(content)}

def extract_text_from_txt(file):
    return {"job_description": file.read().decode("utf-8", errors="ignore")}

def process_uploaded_file(uploaded_file):
    if not uploaded_file:
        return {"job_description": ""}
    ext = uploaded_file.name.split(".")[-1].lower()
    if ext == "pdf":
        return extract_text_from_pdf(uploaded_file)
    elif ext == "docx":
        return extract_text_from_docx(uploaded_file)
    elif ext == "txt":
        return extract_text_from_txt(uploaded_file)
    else:
        return {"job_description": f"Unsupported format: {ext}"}

def extract_content_from_url(url):
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        clean_text = re.sub(r"<.*?>", "", resp.text)  # strip HTML tags
        return clean_text
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching URL: {e}")
        return ""

# -------------------------
# LLM Integration
# -------------------------
OLLAMA_API_URL = "http://127.0.0.1:11434/api/generate"

def fetch_from_llama(prompt):
    """
    Example call to a local LLaMA model via Ollama.
    Adjust 'model' or parameters as needed.
    """
    payload = {
        "model": "llama2:7b",
        "prompt": prompt,
        "num_ctx": 512,
        "num_predict": 256,
        "stream": False
    }
    try:
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=120)
        response.raise_for_status()
        data = json.loads(response.text)
        return data.get("response", "No valid response.")
    except requests.exceptions.RequestException as e:
        st.error(f"Error contacting LLM: {e}")
        return ""
