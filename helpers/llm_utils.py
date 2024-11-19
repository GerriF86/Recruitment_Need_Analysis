import requests
import json
import streamlit as st
from typing import List

def query_local_llm(prompt: str, model: str = "koesn/dolphin-llama3-8b", num_ctx: int = 8192) -> str:
    # Implementation same as before with correct error handling and response parsing
    ...

def query_remote_api(prompt: str, api_key: str, timeout: int = 15) -> str:
    # Implementation same as before with correct error handling and response parsing
    ...

def query_rag(prompt: str, api_key: str, retrieval_count: int = 5, confidence_threshold: float = 0.5) -> str:
    # Implementation same as before with correct error handling and response parsing
    ...

def generate_role_skills(role: str) -> List[str]:
    if not role:
        st.warning("Role is empty. Please provide a valid job role.")
        return []
    prompt = f"List 20 essential skills required for the role: {role}."
    skills_response = query_model(prompt)
    if not skills_response:
        st.error("Failed to generate skills. Ensure the model server is running.")
        return []
    skills = [skill.strip() for skill in skills_response.split("\n") if skill.strip()]
    return skills or ["No skills found. Please try a different role."]

def generate_section_summary(section: str, details: str) -> str:
    if not details:
        return f"No details provided for {section}."
    prompt = f"Summarize the following {section} details:\n{details}"
    summary = query_model(prompt)
    if not summary:
        st.error(f"Failed to generate a summary for {section}.")
        return f"Unable to summarize {section}. Please review the details."
    return summary

def generate_job_advertisement(company_info: str, role_info: str, benefits: str, recruitment_process: str) -> str:
    if not any([company_info, role_info, benefits, recruitment_process]):
        return "Insufficient data to generate a job advertisement."
    prompt = f"""
    Write a professional job advertisement with the following details, presented and phrased in a way that attracts the target group and automatically attach an (m/w/d) at the end of the job title:

    Company Information:
    {company_info}

    Role Information:
    {role_info}

    Benefits:
    {benefits}

    Recruitment Process:
    {recruitment_process}
    """
    job_ad = query_model(prompt)
    if not job_ad:
        st.error("Failed to generate the job advertisement. Please check your inputs.")
        return "Job advertisement generation failed. Please try again."
    return job_ad
