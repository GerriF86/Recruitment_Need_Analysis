# prompts.py

from functions import fetch_from_llama

def generate_job_ad(session_data):
    """
    Generate a job ad from the session data.
    This is a simple version. Extend or refine as needed.
    """
    job_title = session_data.get("job_title", "No Title")
    company_name = session_data.get("company_name", "No Company")
    location = session_data.get("location", "")
    benefits = session_data.get("benefits", "")
    tasks = session_data.get("tasks", "")
    responsibilities = session_data.get("responsibility_distribution", "")
    
    prompt = f"""
    You are an AI specialized in HR. Create a compelling job ad for the following role:
    Job Title: {job_title}
    Company: {company_name}
    Location: {location}
    Responsibilities: {responsibilities}
    Key Tasks: {tasks}
    Benefits: {benefits}
    Make it engaging and concise. Return a plain text version.
    """
    return fetch_from_llama(prompt)

def generate_interview_prep(session_data, audience="HR"):
    """
    Generate an interview preparation guide from session data.
    Audience might be 'HR', 'Technical', etc.
    """
    job_title = session_data.get("job_title", "No Title")
    tasks = session_data.get("tasks", "")
    responsibilities = session_data.get("responsibility_distribution", "")
    
    prompt = f"""
    You are an AI specialized in recruitment. Generate an interview preparation guide
    for a {job_title} role aimed at {audience} interviewers. The role has these key tasks:
    {tasks}
    And these responsibilities:
    {responsibilities}
    Return a structured, step-by-step guide in plain text.
    """
    return fetch_from_llama(prompt)
