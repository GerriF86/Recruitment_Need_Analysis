import streamlit as st
import sys
from pathlib import Path
from helpers.state_management import change_page, cached_generate_role_skills  # Updated to correct helper
from helpers.llm_utils import query_local_llm, query_remote_api, query_rag  # LLM-related functions
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Dynamically add the project root to the Python path to fix import issues
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Load Groq API key
groq_key = os.getenv("groq_key")
if not groq_key:
    groq_key = st.sidebar.text_input("Enter Groq API Key:", type="password")
    if groq_key:
        st.session_state["groq_key"] = groq_key

# Page Configuration
st.set_page_config(page_title="Recruitment Need Analysis", page_icon="📄", layout="wide")

# Initialize Session State
session_keys = ["page", "company_info", "role_info", "benefits", "recruitment_process", "model_type"]
for key in session_keys:
    st.session_state.setdefault(key, 1 if key == "page" else None)

# Function to query models dynamically
def query_model(prompt: str) -> str:
    if st.session_state.model_type == "Local LLM":
        return query_local_llm(prompt)
    elif st.session_state.model_type == "Remote API via Groq":
        return query_remote_api(prompt, groq_key)
    elif st.session_state.model_type == "RAG":
        return query_rag(prompt, groq_key)
    else:
        st.error("Invalid model type selected.")
        return ""

# Main App Logic for Recruitment Need Analysis
from helpers.ui_components import (
    company_info_page,
    role_info_page,
    benefits_page,
    recruitment_process_page,
    summary_page,
    job_ad_page
)

pages = {
    1: company_info_page,
    2: role_info_page,
    3: benefits_page,
    4: recruitment_process_page,
    5: summary_page,
    6: job_ad_page,
}

current_page = st.session_state.page
pages.get(current_page, company_info_page)()

# Footer Styling
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)
