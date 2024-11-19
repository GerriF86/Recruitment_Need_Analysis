import re
import os
import requests
import streamlit as st
from typing import List, Optional
import json


def validate_job_title(job_title: str) -> bool:
    """Validate the job title to ensure it follows an appropriate format."""
    return bool(re.match(r"^[A-Za-z0-9 ]+$", job_title))


def format_response(response: dict) -> str:
    """Format the response dictionary into a presentable HTML format."""
    return f"""
    <div>
        <h3>Job Title: {response.get('job_title', 'N/A')}</h3>
        <p>Responsibilities: {', '.join(response.get('responsibilities', []))}</p>
        <p>Skills Required: {', '.join(response.get('skills', []))}</p>
        <p>Benefits Offered: {', '.join(response.get('benefits', []))}</p>
    </div>
    """


def extract_keywords_from_text(text: str) -> List[str]:
    """Placeholder for NLP-based keyword extraction from a given text input."""
    return ["Leadership", "Team Management", "Critical Thinking"]  # Example


def load_html_template(template_name: str) -> Optional[str]:
    """Load an HTML template from the templates directory."""
    try:
        with open(os.path.join("templates", template_name), "r") as html_file:
            return html_file.read()
    except FileNotFoundError:
        st.error(f"Template '{template_name}' not found. Please ensure it exists in the 'templates' directory.")
        return None


def query_local_llm(prompt: str, model: str = "koesn/dolphin-llama3-8b", num_ctx: int = 8192) -> str:
    """
    Query a local LLM server to generate a response based on a prompt.

    Args:
        prompt (str): Input prompt for the LLM.
        model (str): Model name to use for generation.
        num_ctx (int): Context length for the model.

    Returns:
        str: Generated response from the LLM.
    """
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


def generate_role_skills(role: str) -> List[str]:
    """
    Generate a list of key skills for a specific role using the local LLM.

    Args:
        role (str): The job role to generate skills for.

    Returns:
        List[str]: A list of skills or an empty list if generation fails.
    """
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


def generate_section_summary(section: str, details: str) -> str:
    """
    Generate a summary for a specific section using the local LLM.

    Args:
        section (str): The name of the section to summarize.
        details (str): Details to include in the summary.

    Returns:
        str: A summary of the section or an error message if generation fails.
    """
    if not details:
        return f"No details provided for {section}."

    prompt = f"Summarize the following {section} details:\n{details}"
    summary = query_local_llm(prompt)

    if not summary:
        st.error(f"Failed to generate a summary for {section}.")
        return f"Unable to summarize {section}. Please review the details."

    return summary


def generate_job_advertisement(company_info: str, role_info: str, benefits: str, recruitment_process: str) -> str:
    """
    Generate a professional job advertisement using provided inputs.

    Args:
        company_info (str): Summary of the company information.
        role_info (str): Summary of the role information.
        benefits (str): List of benefits offered.
        recruitment_process (str): Description of the recruitment process.

    Returns:
        str: A job advertisement or an error message if generation fails.
    """
    if not any([company_info, role_info, benefits, recruitment_process]):
        return "Insufficient data to generate a job advertisement."

    prompt = f"""
    Write a professional job advertisement with the following details, presented and phrased in a way that attracts the target group and automatically attach an (m/w/d) at the end of the jobtitle:

    Company Information:
    {company_info}

    Role Information:
    {role_info }

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