# Job_Ad_Generator.py
import json
import requests
from flask import Blueprint, render_template_string, request

job_ad_generator_bp = Blueprint('job_ad_generator', __name__)

# Load configuration from config.json
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

@job_ad_generator_bp.route('/generate_job_ad', methods=['POST'])
def generate_job_ad():
    # Gather job details from form submission
    role = request.form.get('role')
    skills = request.form.getlist('skills')
    benefits = request.form.getlist('benefits')

    # Prepare prompt for LLM
    prompt = f"Create a job ad for a {role} position. Key skills include {', '.join(skills)}. Benefits are: {', '.join(benefits)}."

    # Use the correct URL for the local LLM API
    api_url = "http://localhost:11434/api/generate"  # Update to use the correct endpoint
    payload = {
        "prompt": prompt,
        "config_id": config.get("id")  # Including the config_id from config.json
    }
    headers = {
        "Content-Type": "application/json"
    }

    # Send request to the local LLM
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes
        llm_output = response.json()
        job_ad = llm_output.get("generated_text", "No text generated.")
    except requests.RequestException as e:
        job_ad = f"An error occurred while generating the job ad: {e}"

    return render_template('job_ad.html', role=role, job_ad=job_ad)
