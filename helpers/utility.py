# helpers/utility.py
import re

def validate_job_title(job_title):
    """
    Validate the job title to ensure it follows appropriate format (e.g., no special characters).
    """
    if re.match("^[A-Za-z0-9 ]+$", job_title):
        return True
    return False

def format_response(response):
    """
    Format the response dictionary into a presentable HTML or JSON format.
    """
    formatted_response = f"<div><h3>Job Title: {response['job_title']}</h3>"
    formatted_response += f"<p>Responsibilities: {', '.join(response['responsibilities'])}</p>"
    formatted_response += f"<p>Skills Required: {', '.join(response['skills'])}</p>"
    formatted_response += f"<p>Benefits Offered: {', '.join(response['benefits'])}</p></div>"
    return formatted_response

def extract_keywords_from_text(text):
    """
    Placeholder for NLP-based keyword extraction from a given text input.
    Leverage trained NLP model to pull key attributes about job responsibilities, skills, etc.
    """
    # Assuming an NLP model is available for extracting key information from input text.
    keywords = ["Leadership", "Team Management", "Critical Thinking"]  # Example output
    return keywords