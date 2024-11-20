import os
import re
import requests
import json
import streamlit as st
from typing import List, Dict, Optional
from pathlib import Path

# Query Functions
def query_local_llm(prompt: str, model: str = "koesn/dolphin-llama3-8b", num_ctx: int = 8192) -> str:
    """Query a local LLM server to generate a response based on a prompt."""
    url = "http://127.0.0.1:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    payload = {"model": model, "prompt": prompt, "num_ctx": num_ctx}

    try:
        response = requests.post(url, headers=headers, json=payload, stream=True)
        response.raise_for_status()

        generated_text = ""
        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode("utf-8"))
                generated_text += data.get("response", "")
                if data.get("done", False):
                    break
        return generated_text.strip()
    except requests.RequestException as e:
        st.error(f"Error connecting to the LLM server: {e}")
        return ""
    except json.JSONDecodeError as e:
        st.error(f"Error decoding LLM response: {e}")
        return ""

def query_remote_api(prompt: str, api_key: str, timeout: int = 15) -> str:
    """Query a remote API to generate a response based on a prompt."""
    # Placeholder for future implementation
    st.info("Remote API integration not yet implemented.")
    return ""

def query_rag(prompt: str, api_key: str, retrieval_count: int = 5, confidence_threshold: float = 0.5) -> str:
    """Query a Retrieval-Augmented Generation (RAG) API."""
    # Placeholder for future implementation
    st.info("RAG integration not yet implemented.")
    return ""

# Skill and Summary Generators
@st.cache_data
def cached_generate_role_skills(role: str) -> List[str]:
    """Generate and cache skills for a specific role."""
    if not role:
        st.warning("Role is empty. Please provide a valid job role.")
        return []

    prompt = f"List 10 essential skills required for the role: {role}."
    skills_response = query_local_llm(prompt)

    if not skills_response:
        st.error("Failed to generate skills. Ensure the LLM server is running.")
        return []

    skills = [skill.strip() for skill in skills_response.split("\n") if skill.strip()]
    return skills or ["No skills found. Please try a different role."]

def categorize_skills(skills: List[str]) -> Dict[str, List[str]]:
    """Categorize skills into predefined categories."""
    categories = {
        "Technical Skills": [],
        "Soft Skills": [],
        "Management Skills": [],
        "Industry Knowledge": [],
        "Miscellaneous": [],
    }
    for skill in skills:
        if "tech" in skill.lower():
            categories["Technical Skills"].append(skill)
        elif "soft" in skill.lower():
            categories["Soft Skills"].append(skill)
        elif "manager" in skill.lower():
            categories["Management Skills"].append(skill)
        elif "industry" in skill.lower():
            categories["Industry Knowledge"].append(skill)
        else:
            categories["Miscellaneous"].append(skill)
    return categories

# Utility Functions
def validate_job_title(job_title: str) -> bool:
    """Validate the job title to ensure it follows an appropriate format."""
    return bool(re.match(r"^[A-Za-z0-9 ]+$", job_title))

def load_html_template(template_name: str) -> Optional[str]:
    """Load an HTML template from the templates directory."""
    try:
        with open(os.path.join("templates", template_name), "r") as html_file:
            return html_file.read()
    except FileNotFoundError:
        st.error(f"Template '{template_name}' not found. Please ensure it exists in the 'templates' directory.")
        return None

# Job Advertisement Generator
def generate_job_advertisement(company_info: str, role_info: str, benefits: str, recruitment_process: str) -> str:
    """Generate a professional job advertisement using provided inputs."""
    if not any([company_info, role_info, benefits, recruitment_process]):
        return "Insufficient data to generate a job advertisement."

    prompt = f"""
    Write a professional job advertisement with the following details, phrased to attract the target group, and add (m/w/d) to the job title:

    Company Information:
    {company_info}

    Role Information:
    {role_info}

    Benefits:
    {benefits}

    Recruitment Process:
    {recruitment_process}
    """
    job_ad = query_local_llm(prompt)

    if not job_ad:
        st.error("Failed to generate the job advertisement. Please check your inputs.")
        return "Job advertisement generation failed. Please try again."

    return job_ad
def custom_css():
    """Apply custom CSS styling to the Streamlit app."""
    st.markdown(
        """
        <style>
        body {
            background-color: #f9f9f9;
        }
        header, footer {
            visibility: hidden;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )