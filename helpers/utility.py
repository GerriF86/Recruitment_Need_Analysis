import re
import os
import requests
import streamlit as st
from typing import List, Optional

def validate_job_title(job_title: str) -> bool:
    """
    Validate the job title to ensure it follows an appropriate format (e.g., no special characters).

    Parameters:
        job_title (str): The job title string to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    return bool(re.match("^[A-Za-z0-9 ]+$", job_title))

def format_response(response: dict) -> str:
    """
    Format the response dictionary into a presentable HTML format.

    Parameters:
        response (dict): A dictionary containing job ad data.

    Returns:
        str: A formatted HTML representation of the response.
    """
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
    """
    Extract key attributes about job responsibilities, skills, etc. using an NLP model.

    Parameters:
        text (str): The input text from which to extract keywords.

    Returns:
        List[str]: Extracted keywords from the text.
    """
    # Placeholder logic for keyword extraction (Replace with actual NLP model code if available)
    keywords = ["Leadership", "Team Management", "Critical Thinking"]  # Example output
    return keywords

def load_html_template(template_name: str) -> Optional[str]:
    """
    Load an HTML template from the templates directory.

    Parameters:
        template_name (str): The name of the HTML file to load (e.g., 'Impressum.html').

    Returns:
        Optional[str]: The HTML content of the file if found, otherwise None.
    """
    try:
        with open(os.path.join("templates", template_name), "r") as html_file:
            return html_file.read()
    except FileNotFoundError:
        st.error(f"{template_name} template not found. Please ensure the file is located in the 'templates' directory.")
        return None

def generate_job_ad_from_llm(prompt: str) -> str:
    """
    Generate a job ad using the local LLM via the API.

    Parameters:
        prompt (str): The prompt for the LLM to generate text.

    Returns:
        str: The generated text or an error message if the request failed.
    """
    API_URL = os.getenv('LLM_API_URL', 'http://localhost:11434/api/generate')
    payload = {"prompt": prompt}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()
        llm_output = response.json()
        return llm_output.get("generated_text", "No text generated.")
    except requests.ConnectionError:
        return "A connection error occurred while generating the job ad."
    except requests.Timeout:
        return "The request to the LLM timed out. Please try again later."
    except requests.RequestException as e:
        return f"An error occurred while generating the job ad: {e}"

def sanitize_input(input_text: str) -> str:
    """
    Sanitize user input to prevent security issues like script injection.

    Parameters:
        input_text (str): The user-provided text to sanitize.

    Returns:
        str: The sanitized text.
    """
    sanitized_text = re.sub(r'[<>]', '', input_text)  # Remove < and > to prevent script injection
    return sanitized_text

def log_response(response: dict, log_file: str = "responses.log") -> None:
    """
    Log the generated job ad response to a file.

    Parameters:
        response (dict): The response dictionary to log.
        log_file (str): The name of the file to store logs (default is 'responses.log').
    """
    try:
        with open(log_file, "a") as f:
            f.write(f"{response}\n")
    except Exception as e:
        st.error(f"An error occurred while logging the response: {e}")
