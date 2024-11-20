import os
import re
import requests
import json
import streamlit as st
from typing import List, Dict, Optional
from pathlib import Path

# Function to query the Groq API with enhanced error handling and debugging
def query_groq_model(prompt, model_name="llama3-8b-8192"):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {groq_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model_name,
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        response_data = response.json()
        return response_data["choices"][0]["message"]["content"]
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        st.error(f"Request error occurred: {req_err}")
    except ValueError as json_err:
        st.error(f"JSON decode error: {json_err}")
    return None

# Query Functions
@st.cache_data
def cached_generate_role_skills(role: str) -> Dict[str, List[str]]:
    """Generate and cache skills for a specific role."""
    if not role:
        return {"Error": ["No role specified."]}

    categories = {
        "Programming Languages": [],
        "Libraries": [],
        "Soft Skills": [],
        "Technical Skills": [],
        "Management Skills": [],
        "Analytical Skills": [],
        "Tools/Technologies": []
    }

    prompt = (
        f"You are an expert HR consultant. For the role '{role}', list as keywords with no further explanation the top 5 Programming Languages, "
        f"top 15 Libraries, and top 10 Soft Skills, along with other skills categorized as "
        f"Technical Skills, Management Skills, Analytical Skills, and Tools/Technologies."
    )

    skills_response = query_local_llm(prompt)
    skills = [skill.strip() for skill in skills_response.split("\n") if skill.strip()]
    
    predefined_keywords = {
        "Programming Languages": ["Python", "Java", "C++", "JavaScript", "SQL"],
        "Libraries": ["TensorFlow", "PyTorch", "Scikit-learn", "Pandas", "NumPy"],
        "Soft Skills": ["communication", "teamwork", "adaptability", "problem-solving"],
        "Technical Skills": ["programming", "coding", "cloud", "networking", "engineering"],
        "Management Skills": ["leadership", "planning", "strategy", "risk management"],
        "Analytical Skills": ["data", "analysis", "decision-making", "quantitative"],
        "Tools/Technologies": ["Excel", "Tableau", "Power BI", "SQL", "Python"]
    }

    # Categorize skills into predefined sections
    for skill in skills:
        for category, keywords in predefined_keywords.items():
            if any(keyword.lower() in skill.lower() for keyword in keywords):
                if len(categories[category]) < 15:  # Allow up to 15 items
                    categories[category].append(skill)
                break

    return categories

def role_info_page(role: str):
    """Render the Role Information page with sliders for skill intensity."""
    skills_categories = cached_generate_role_skills(role)

    if "Error" in skills_categories:
        st.warning("No role specified or skills could not be generated.")
        return

    skill_levels = {}
    for category, skill_list in skills_categories.items():
        st.markdown(f"### {category}")
        for skill in skill_list:
            # Sliders are moved outside the cached function
            skill_levels[skill] = st.slider(
                f"{skill} (Nice to Have ↔ Must Have)",
                min_value=0,
                max_value=10,
                value=5
            )
    
    # Optionally cache the skill levels in `st.session_state`
    st.session_state[f"{role}_skill_levels"] = skill_levels

def generate_interview_preparation_sheet(data: Dict[str, any]) -> str:
    """
    Generate an interview preparation sheet based on the gathered information.

    Args:
        data (Dict[str, Any]): A dictionary containing gathered information. Example keys:
            - "job_title"
            - "role_requirements"
            - "company_benefits"
            - "recruitment_steps"
            - "candidate_attributes"
            - "additional_notes"

    Returns:
        str: A formatted interview preparation sheet.
    """
    # Ensure `query_local_llm` is accessible
    try:
        from helpers.utils import query_local_llm
    except ImportError:
        st.error("The `query_local_llm` function is missing or not properly imported.")
        return ""

    # Validate input data
    required_keys = ["job_title", "role_requirements", "company_benefits", "recruitment_steps", "candidate_attributes"]
    missing_keys = [key for key in required_keys if key not in data]
    if missing_keys:
        st.error(f"Missing required keys in data: {', '.join(missing_keys)}")
        return ""

    # Prepare the prompt for the LLM
    prompt = f"""
    You are an HR assistant helping to create a structured interview preparation sheet.
    Based on the following information, generate a detailed preparation document for the interviewer:
    
    Job Title: {data.get("job_title", "N/A")}
    Role Requirements: {data.get("role_requirements", "N/A")}
    Company Benefits: {data.get("company_benefits", "N/A")}
    Recruitment Steps: {data.get("recruitment_steps", "N/A")}
    Candidate Attributes: {data.get("candidate_attributes", "N/A")}
    Additional Notes: {data.get("additional_notes", "None")}
    
    Format the preparation sheet into sections such as:
    - Overview of the Role
    - Key Responsibilities
    - Candidate Requirements
    - Benefits and Incentives
    - Interview Structure
    - Additional Notes
    
    Provide the document in a clean and professional tone.
    """

    # Query the local LLM
    try:
        preparation_sheet = query_local_llm(prompt)
        if not preparation_sheet or len(preparation_sheet.strip()) == 0:
            raise ValueError("The LLM returned an empty or invalid response.")
    except Exception as e:
        st.error(f"Error while querying the local LLM: {e}")
        return ""

    return preparation_sheet

def query_local_llm(prompt: str, model: str = "koesn/dolphin-llama3-8b", num_ctx: int = 8192) -> str:
    """Query a local LLM server to generate a response as keywords with no further explanation based on a prompt."""
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
def user_model_query(prompt):
    if st.session_state.model_choice == "Local Ollama (High Quality, Slower)":
        # Use local model
        response = query_local_llm(prompt)
    elif st.session_state.model_choice == "Groq llama3-8b (Fast, Slightly Lower Quality)":
        # Use Groq's llama3-8b model
        response = query_groq_model(prompt, model_name="llama3-8b")
    else:
        response = "Invalid model choice"
    return response

def query_remote_api(prompt: str, api_key: str, timeout: int = 15) -> str:
    """Query a remote API to generate a response based on a prompt."""
    st.info("Remote API integration not yet implemented.")
    return ""

def query_rag(prompt: str, api_key: str, retrieval_count: int = 5, confidence_threshold: float = 0.5) -> str:
    """Query a Retrieval-Augmented Generation (RAG) API."""
    st.info("RAG integration not yet implemented.")
    return ""

# Skill and Summary Generators
@st.cache_data
def cached_generate_role_skills(role: str) -> Dict[str, List[str]]:
    """Generate as keywords with no further explanation and cache skills for a specific role with sliders for intensity adjustments."""
    if not role:
        st.warning("Role is empty. Please provide a valid job role.")
        return {"Error": ["No role specified."]}

    categories = {
        "Programming Languages": [],
        "Libraries": [],
        "Soft Skills": [],
        "Technical Skills": [],
        "Management Skills": [],
        "Analytical Skills": [],
        "Tools/Technologies": []
    }

    # Updated prompt to align with specific categories
    prompt = (
        f"You are an expert HR consultant. For the role '{role}', list as keywords with no further explanation the top 5 Programming Languages, "
        f"top 15 Libraries, and top 10 Soft Skills, along with other skills categorized as "
        f"Technical Skills, Management Skills, Analytical Skills, and Tools/Technologies."
    )

    try:
        skills_response = query_local_llm(prompt)
        if not isinstance(skills_response, str) or len(skills_response.strip()) == 0:
            raise ValueError("Invalid or empty LLM response.")

        skills = [skill.strip() for skill in skills_response.split("\n") if skill.strip()]
        if not skills:
            raise ValueError("Empty skill list generated.")

        predefined_keywords = {
            "Programming Languages": ["Python", "Java", "C++", "JavaScript", "SQL"],
            "Libraries": ["TensorFlow", "PyTorch", "Scikit-learn", "Pandas", "NumPy"],
            "Soft Skills": ["communication", "teamwork", "adaptability", "problem-solving"],
            "Technical Skills": ["programming", "coding", "cloud", "networking", "engineering"],
            "Management Skills": ["leadership", "planning", "strategy", "risk management"],
            "Analytical Skills": ["data", "analysis", "decision-making", "quantitative"],
            "Tools/Technologies": ["Excel", "Tableau", "Power BI", "SQL", "Python"]
        }

        # Categorize skills into predefined sections
        for skill in skills:
            added = False
            for category, keywords in predefined_keywords.items():
                if any(keyword.lower() in skill.lower() for keyword in keywords):
                    if len(categories[category]) < 15:  # Allow up to 15 for Libraries and others
                        categories[category].append(skill)
                        added = True
                        break

            if not added and len(categories["Tools/Technologies"]) < 15:
                categories["Tools/Technologies"].append(skill)

        # UI to prioritize and adjust skill levels
        st.subheader(f"Skills for {role}")
        skill_levels = {}

        for category, skill_list in categories.items():
            st.markdown(f"### {category}")
            for skill in skill_list:
                skill_levels[skill] = st.slider(
                    f"{skill} (Nice to Have ↔ Must Have)",
                    min_value=0,
                    max_value=10,
                    value=5
                )

        # Cache skill adjustments as a dictionary
        st.session_state[f"{role}_skills"] = skill_levels

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

def change_page(new_page: int):
    """Changes the current page."""
    st.session_state.page = new_page

# Generate and Cache Role-Specific Benefits
@st.cache_data
def cached_generate_role_benefits(role: str):
    """
    Generate and cache a list of keywords with no further explanation role-specific benefits, described with less than 5 words.
    """
    if not role:
        st.warning("Role is empty. Please provide a valid job role.")
        return ["No role specified."]

    # Construct the prompt
    prompt = (
        f"You are an expert HR consultant. List up to 10 benefits as keywords with no further explanation that would attract candidates "
        f"to the role '{role}'. Provide them as bullet points."
    )

    # Query the LLM
    try:
        benefits_response = query_local_llm(prompt)
        if not isinstance(benefits_response, str) or len(benefits_response.strip()) == 0:
            raise ValueError("Invalid or empty LLM response.")

        # Split response into lines and clean them
        benefits = [benefit.strip() for benefit in benefits_response.split("\n") if benefit.strip()]
        if not benefits:
            raise ValueError("Empty benefit list generated.")

        # Limit benefits to 10 items
        return benefits[:10]

    except Exception as e:
        st.error(f"Error generating benefits: {e}")
        return ["No benefits could be generated due to a processing error."]

# Generate and Cache Role-Specific Recruitment Steps
@st.cache_data
def cached_generate_role_recruitment_steps(role: str):
    """
    Generate and cache a list of role-specific recruitment steps.
    """
    if not role:
        st.warning("Role is empty. Please provide a valid job role.")
        return ["No role specified."]

    # Construct the prompt
    prompt = (
        f"You are an expert HR consultant. List up to 10 ideal steps for the recruitment process as keywords with no further explanation for "
        f"the role '{role}'. Provide them as bullet points."
    )

    # Query the LLM
    try:
        recruitment_steps_response = query_local_llm(prompt)
        if not isinstance(recruitment_steps_response, str) or len(recruitment_steps_response.strip()) == 0:
            raise ValueError("Invalid or empty LLM response.")

        # Split response into lines and clean them
        recruitment_steps = [step.strip() for step in recruitment_steps_response.split("\n") if step.strip()]
        if not recruitment_steps:
            raise ValueError("Empty recruitment step list generated.")

        # Limit steps to 10 items
        return recruitment_steps[:10]

    except Exception as e:
        st.error(f"Error generating recruitment steps: {e}")
        return ["No recruitment steps could be generated due to a processing error."]
