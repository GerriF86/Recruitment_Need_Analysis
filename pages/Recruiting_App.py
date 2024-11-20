import streamlit as st
import toml
import requests
from pathlib import Path
import sys
from helpers.utils import (
    validate_job_title,
    cached_generate_role_skills,
    generate_job_advertisement,
    cached_generate_role_benefits,
    cached_generate_role_recruitment_steps,
    query_local_llm
)

# Dynamically add the project root to the Python path to fix import issues
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Load configurations from config.toml
try:
    config = toml.load("config.toml")
except Exception as e:
    st.error(f"Error loading configuration file: {e}")
    st.stop()

# Set page configuration - use settings from config.toml
st.set_page_config(
    page_title=config["app"]["page_title"],
    page_icon=config["app"]["page_icon"],
    layout=config["app"].get("layout", "wide")
)

# Load the Groq API Key
groq_key = config["api"]["groq_key"]

# Initialize Session State
session_keys = ["page", "company_info", "role_info", "benefits", "recruitment_process", "must_have_skills", "nice_to_have_skills", "selected_benefits", "selected_recruitment_steps", "model_choice"]
for key in session_keys:
    if key not in st.session_state:
        st.session_state[key] = [] if key in ["must_have_skills", "nice_to_have_skills", "selected_benefits", "selected_recruitment_steps"] else None

# Model Selection by User
model_choice = st.selectbox(
    "Select Model Type:",
    options=["Olivia an Gerrits LLM (High Quality, Slow Performance)", "Groq llama (Standard Quality, Fast Performance)"],
    key="model_choice"
)

# Function to use the appropriate model based on user selection
def user_model_query(prompt):
    if st.session_state.model_choice == "Local Ollama (High Quality, Slower)":
        # Use local model
        return query_local_llm(prompt)
    elif st.session_state.model_choice == "Groq llama3-8b (Fast, Slightly Lower Quality)":
        # Use Groq model via API
        return query_groq_model(prompt, model_name="llama3-8b")
    else:
        return "Invalid model choice"

# UI for User Prompt and Generating Response
st.title("Recruitment Need Analysis - Model Interaction")

# Page functions
def change_page(new_page: int):
    """Function to change the page in the app."""
    st.session_state.page = new_page

def company_info_page():
    st.title("Company Information")
    company_name = st.text_input("Company Name:")
    location = st.text_input("Location:")
    industry = st.text_input("Industry:")

    company_size = st.slider(
        "Number of Employees:",
        min_value=1,
        max_value=1000,
        value=200,
        step=10,
        help="Slide to select the approximate number of employees."
    )

    if st.button("Next"):
        if not company_name or not location or not industry:
            st.error("Please fill out all fields.")
            return

        st.session_state.company_info = {
            "company_name": company_name,
            "location": location,
            "industry": industry,
            "company_size": company_size,
        }
        change_page(2)  # Move to the next page

def role_info_page():
    st.title("Role Information")
    
    # Job Role Title
    role = st.text_input("Role Title:", placeholder="e.g., Data Scientist")
    
    # Salary Range Input using a Slider
    st.markdown("### Salary Expectation")
    salary_range = st.slider(
        "Select the salary range:",
        min_value=30000,
        max_value=500000,
        value=(50000, 150000),
        step=10000,
        help="Move the sliders to set the minimum and maximum salary expectations."
    )
    salary_min, salary_max = salary_range

    # Place of Work
    place_of_work = st.text_input(
        "Place of Work:",
        placeholder="e.g., Berlin, Germany",
        help="Enter the location where the job will be performed."
    )

    # Type of Work
    st.markdown("### Type of Work")
    work_type = st.radio(
        "Select the work type:",
        options=["Onsite", "Remote", "Hybrid"],
        help="Specify whether the job is onsite, remote, or hybrid."
    )

    # Job Contract Type
    st.markdown("### Job Contract Type")
    contract_type = st.radio(
        "Contract Type:",
        options=["Permanent", "Temporary", "Freelance", "Internship"],
        help="Specify the type of contract for the job."
    )

    # Weekly Hours
    st.markdown("### Weekly Work Hours")
    weekly_hours = st.slider(
        "Select the number of weekly hours:",
        min_value=10,
        max_value=60,
        value=40,
        step=5,
        help="Slide to adjust the average number of hours per week."
    )

    # Additional Perks or Notes
    st.markdown("### Additional Notes or Perks")
    additional_notes = st.text_area(
        "Enter any additional information about the role:",
        placeholder="e.g., Flexible working hours, health insurance, relocation support, etc."
    )

    # Validate and Proceed to the Next Step
    if st.button("Next"):
        if not role or not place_of_work:
            st.error("Please provide the Role Title and Place of Work.")
            return

        # Save data in session state
        st.session_state.role_info = {
            "role": role,
            "salary_min": salary_min,
            "salary_max": salary_max,
            "place_of_work": place_of_work,
            "work_type": work_type,
            "contract_type": contract_type,
            "weekly_hours": weekly_hours,
            "additional_notes": additional_notes.strip()
        }

        change_page(3)  # Move to the next page

def benefits_page():
    st.title("Benefits")
    role = st.session_state.role_info.get("role") if "role_info" in st.session_state else ""

    if role:
        st.write("Role-Specific Benefits Suggestions:")
        benefits_suggestions = cached_generate_role_benefits(role)

        # Display categorized benefits
        st.markdown("### Suggested Benefits:")
        selected_benefits = []
        for benefit in benefits_suggestions:
            if st.checkbox(benefit, key=f"benefit_{benefit}", value=benefit in st.session_state.selected_benefits):
                selected_benefits.append(benefit)
        st.session_state.selected_benefits = selected_benefits

    additional_benefits = st.text_area("Enter any additional benefits you wish to add:")

    if st.button("Next"):
        if not selected_benefits and not additional_benefits:
            st.error("Please select or enter some benefits.")
            return

        st.session_state.benefits = selected_benefits + additional_benefits.split(",")
        change_page(4)  # Move to the next page

def recruitment_process_page():
    st.title("Recruitment Process")
    role = st.session_state.role_info.get("role") if "role_info" in st.session_state else ""

    if role:
        st.write("Role-Specific Recruitment Process Suggestions:")
        recruitment_steps_suggestions = cached_generate_role_recruitment_steps(role)

        # Display categorized recruitment steps
        st.markdown("### Suggested Recruitment Steps:")
        selected_recruitment_steps = []
        for step in recruitment_steps_suggestions:
            if st.checkbox(step, key=f"recruitment_step_{step}", value=step in st.session_state.selected_recruitment_steps):
                selected_recruitment_steps.append(step)
        st.session_state.selected_recruitment_steps = selected_recruitment_steps

    additional_steps = st.text_area("Enter any additional recruitment steps you wish to add:")

    if st.button("Next"):
        if not selected_recruitment_steps and not additional_steps:
            st.error("Please select or enter recruitment steps.")
            return

        st.session_state.recruitment_process = selected_recruitment_steps + additional_steps.split(",")
        change_page(5)  # Move to the next page

def summary_page():
    st.title("Summary of Collected Information")
    st.markdown("### Company Information")
    st.write(st.session_state.get("company_info", "No data provided."))

    st.markdown("### Role Information")
    st.write(st.session_state.get("role_info", "No data provided."))

    st.markdown("### Benefits")
    st.write(st.session_state.get("benefits", "No data provided."))

    st.markdown("### Recruitment Process")
    st.write(st.session_state.get("recruitment_process", "No data provided."))

    st.markdown("### Enter Comments or Adjustments")
    comment = st.text_area("Enter your comments or any adjustments to the collected information:")
    if st.button("Submit Comments"):
        if comment:
            update_summary_with_comments(comment)
            st.success("Comments added successfully!")

    if st.button("Next"):
        change_page(6)  # Move to the next page

def job_ad_page():
    st.title("Generated Job Advertisement")
    if all(key in st.session_state for key in ["company_info", "role_info", "benefits", "recruitment_process"]):
        job_ad = generate_job_advertisement(
            company_info=str(st.session_state.company_info),
            role_info=str(st.session_state.role_info),
            benefits=str(st.session_state.benefits),
            recruitment_process=str(st.session_state.recruitment_process),
        )
        st.write("Job Advertisement:")
        st.write(job_ad)
        st.download_button("Download Job Advertisement", job_ad, file_name="job_advertisement.txt")
    else:
        st.error("Incomplete information. Please fill out all sections.")

def iv_prep_page():
    st.title("Interview Preparation Sheet")
    if all(key in st.session_state for key in ["company_info", "role_info", "benefits", "recruitment_process"]):
        iv_prep = generate_interview_preparation_sheet(
            company_info=str(st.session_state.company_info),
            role_info=str(st.session_state.role_info),
            benefits=str(st.session_state.benefits),
            recruitment_process=str(st.session_state.recruitment_process),
        )
        st.write("Interview Preparation Sheet:")
        st.write(iv_prep)
        st.download_button("Download Interview Preparation Sheet", job_ad, file_name="Interview Preparation Sheet.txt")
    else:
        st.error("Incomplete information. Please fill out all sections.")

# Function to update summary with comments
def update_summary_with_comments(comment: str):
    """
    This function processes the comments entered by the user and makes adjustments
    to the session state data accordingly. 
    """
    if "adjust company name" in comment.lower():
        new_company_name = st.text_input("Enter the new Company Name:")
        if new_company_name:
            st.session_state.company_info["company_name"] = new_company_name

    # Extend logic to cover other fields and adjustments

# Page Mapping
pages = {
    1: company_info_page,
    2: role_info_page,
    3: benefits_page,
    4: recruitment_process_page,
    5: summary_page,
    6: job_ad_page,
    7: iv_prep_page
}

# Render the current page
current_page = st.session_state.page
pages.get(current_page, company_info_page)()

# Footer Styling
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)
