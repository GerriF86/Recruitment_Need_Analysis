# Job_Ad_Generator.py
import os
import json
import requests
from flask import Blueprint, render_template_string, request

job_ad_generator_bp = Blueprint('job_ad_generator', __name__)

# Load LLM API URL from environment variable
API_URL = os.getenv('LLM_API_URL', 'http://localhost:11434/api/generate')  # Default to the local URL if no env variable is found

@job_ad_generator_bp.route('/generate_job_ad', methods=['POST'])
def generate_job_ad():
    # Gather job details from form submission
    role = request.form.get('role')
    skills = request.form.getlist('skills')
    benefits = request.form.getlist('benefits')

    # Prepare prompt for LLM
    prompt = f"Create a job ad for a {role} position. Key skills include {', '.join(skills)}. Benefits are: {', '.join(benefits)}."

    payload = {
        "prompt": prompt
    }
    headers = {
        "Content-Type": "application/json"
    }

    # Use the API URL (either default or from environment variable)
    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()
        llm_output = response.json()
        job_ad = llm_output.get("generated_text", "No text generated.")
    except requests.RequestException as e:
        job_ad = f"An error occurred while generating the job ad: {e}"

    # Return the generated job ad as a response
    return render_template_string('''
    <div class="job-ad-content">
        <h1>Job Ad for {{ role }}</h1>
        <pre>{{ job_ad }}</pre>
    </div>
    ''', role=role, job_ad=job_ad)
