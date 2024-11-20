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
def cached_generate_role_skills(role: str) -> Dict[str, List[str]]:
    """
    Generate and cache skills for a specific role, categorizing them into predefined categories.
    """
    if not role:
        st.warning("Role is empty. Please provide a valid job role.")
        return {"Error": ["No role specified."]}

    # Define role-specific categories
    categories = {
        "Technical Skills": [],
        "Soft Skills": [],
        "Management Skills": [],
        "Analytical Skills": [],
        "Tools/Technologies": []
    }

    # Construct the prompt
    prompt = (
        f"You are an expert HR consultant. List up to 25 skills categorized into "
        f"Technical Skills, Soft Skills, Management Skills, Analytical Skills, "
        f"and Tools/Technologies for the role '{role}'."
    )

    # Query the LLM
    try:
        skills_response = query_local_llm(prompt)
        if not isinstance(skills_response, str) or len(skills_response.strip()) == 0:
            raise ValueError("Invalid or empty LLM response.")

        # Split response into lines and clean them
        skills = [skill.strip() for skill in skills_response.split("\n") if skill.strip()]
        if not skills:
            raise ValueError("Empty skill list generated.")

        # Map skills into categories
        predefined_keywords = {
            "Technical Skills": ["programming", "coding", "cloud", "networking", "engineering"],
            "Soft Skills": ["communication", "teamwork", "adaptability", "problem-solving"],
            "Management Skills": ["leadership", "planning", "strategy", "risk management"],
            "Analytical Skills": ["data", "analysis", "decision-making", "quantitative"],
            "Tools/Technologies": ["Excel", "Tableau", "Power BI", "SQL", "Python"]
        }

        for skill in skills:
            added = False
            for category, keywords in predefined_keywords.items():
                if any(keyword.lower() in skill.lower() for keyword in keywords):
                    if len(categories[category]) < 5:
                        categories[category].append(skill)
                        added = True
                        break

            # Add to Miscellaneous if no specific category matches
            if not added and len(categories["Tools/Technologies"]) < 5:
                categories["Tools/Technologies"].append(skill)

        # Limit total skills across all categories to 25
        total_skills = sum(len(skills) for skills in categories.values())
        if total_skills > 25:
            categories = {k: v[:5] for k, v in categories.items()}

        return categories

    except Exception as e:
        st.error(f"Error generating skills: {e}")
        return {"Error": ["No skills could be generated due to a processing error."]}

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

def change_page(page_number: int):
    """Change the current page of the Streamlit app by updating the session state."""
    if page_number in range(1, 6):
        st.session_state.page = page_number
    else:
        st.error("Invalid page number. Please provide a valid page number between 1 and 5.")
