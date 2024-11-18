import re
import os
import requests
import streamlit as st
from typing import List, Optional
import json


def validate_job_title(job_title: str) -> bool:
    """Validate the job title to ensure it follows an appropriate format."""
    return bool(re.match("^[A-Za-z0-9 ]+$", job_title))


def format_response(response: dict) -> str:
    """Format the response dictionary into a presentable HTML format."""
    formatted_response = f"""
    <div>
        <h3>Job Title: {response.get('job_title', 'N/A')}</h3>
        <p>Responsibilities: {', '.join(response.get('responsibilities', []))}</p>
        <p>Skills Required: {', '.join(response.get('skills', []))}</p>
        <p>Benefits Offered: {', '.join(response.get('benefits', []))}</p>
    </div>
    """
    return formatted_response


def extract_keywords_from_text(text: str) -> List[str]:
    """Placeholder for NLP-based keyword extraction from a given text input."""
    # Replace with actual NLP-based keyword extraction logic.
    keywords = ["Leadership", "Team Management", "Critical Thinking"]  # Example output
    return keywords


def load_html_template(template_name: str) -> Optional[str]:
    """Load an HTML template from the templates directory."""
    try:
        with open(os.path.join("templates", template_name), "r") as html_file:
            return html_file.read()
    except FileNotFoundError:
        st.error(f"{template_name} template not found. Please ensure the file is located in the 'templates' directory.")
        return None


# Utility to query local LLM
def query_local_llm(prompt: str, model: str = "koesn/dolphin-llama3-8b", num_ctx: int = 8192) -> str:
    """
    Sends a query to the local LLM server and returns the response.

    Args:
        prompt (str): The input prompt for the LLM.
        model (str): The model to use (default: "koesn/dolphin-llama3-8b").
        num_ctx (int): The context length for the model (default: 8192).

    Returns:
        str: The generated response from the LLM.
    """
    url = "http://127.0.0.1:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": model,
        "prompt": prompt,
        "num_ctx": num_ctx
    }

    try:
        # Stream request for incremental output
        response = requests.post(url, headers=headers, json=payload, stream=True)
        response.raise_for_status()

        # Accumulate the generated text
        generated_text = ""
        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode("utf-8"))
                generated_text += data.get("response", "")
                if data.get("done", False):
                    break
        return generated_text.strip()
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to LLM: {e}")
        return f"Error connecting to LLM: {e}"
    except json.JSONDecodeError as e:
        st.error(f"Error decoding JSON response: {e}")
        return f"Error decoding JSON response: {e}"


# Function to generate role-specific skills
def generate_role_skills(role: str) -> List[str]:
    """
    Generates a list of 10 skills specific to a role using the local LLM.

    Args:
        role (str): The job role to generate skills for.

    Returns:
        List[str]: A list of role-specific skills.
    """
    prompt = f"List 10 key skills for the role: {role}."
    skills_response = query_local_llm(prompt)
    return skills_response.split("\n") if skills_response else []


# Function to generate section summaries
def generate_section_summary(section: str, details: str) -> str:
    """
    Generates a summary for a given section using the local LLM.

    Args:
        section (str): The section to summarize (e.g., "Company Info").
        details (str): The details to summarize.

    Returns:
        str: A summarized version of the section details.
    """
    prompt = f"Summarize the following {section} information:\n{details}"
    return query_local_llm(prompt)


# Function to create a job advertisement
def generate_job_advertisement(company_info: str, role_info: str, benefits: str, recruitment_process: str) -> str:
    """
    Creates a job advertisement based on the given inputs.

    Args:
        company_info (str): Information about the company.
        role_info (str): Information about the job role.
        benefits (str): List of benefits offered.
        recruitment_process (str): Description of the recruitment process.

    Returns:
        str: A generated job advertisement.
    """
    prompt = f"""
    Create a professional job advertisement using the following details:

    **Company Information:**
    {company_info}

    **Role Information:**
    {role_info}

    **Benefits:**
    {benefits}

    **Recruitment Process:**
    {recruitment_process}
    """
    return query_local_llm(prompt)
