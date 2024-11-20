import streamlit as st
from pathlib import Path
import sys
from helpers.utils import (
    validate_job_title,
    generate_role_skills,
    generate_section_summary,
    generate_job_advertisement,
    change_page,
    load_html_template,
)

# Dynamically add the project root to the Python path to fix import issues
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Set page configuration - This must be the first Streamlit command in the script
st.set_page_config(page_title="Recruitment Need Analysis", page_icon="📄", layout="wide")

# Initialize Session State
session_keys = ["page", "company_info", "role_info", "benefits", "recruitment_process"]
for key in session_keys:
    st.session_state.setdefault(key, 1 if key == "page" else None)

# Page functions
def company_info_page():
    st.title("Company Information")
    company_name = st.text_input("Company Name:")
    location = st.text_input("Location:")
    industry = st.text_input("Industry:")
    company_size = st.number_input("Number of Employees:", min_value=1, step=1)

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

        # Generate and validate section summary
        summary = generate_section_summary("Company Information", str(st.session_state.company_info))
        st.session_state.company_info_summary = summary
        st.write("Summary:", summary)
        change_page(1)

def role_info_page():
    st.title("Role Information")
    role = st.text_input("Role Title:")

    if role and not validate_job_title(role):
        st.error("Invalid role title. Please enter a valid one.")
        return

    if role:
        st.write("Role-Specific Skill Suggestions:")
        skills = generate_role_skills(role)
        st.write(", ".join(skills))

    must_have_skills = st.text_area("Must-Have Skills:")
    nice_to_have_skills = st.text_area("Nice-to-Have Skills:")

    if st.button("Next"):
        if not role or not must_have_skills:
            st.error("Please provide the role and must-have skills.")
            return

        st.session_state.role_info = {
            "role": role,
            "must_have_skills": must_have_skills.split(","),
            "nice_to_have_skills": nice_to_have_skills.split(",") if nice_to_have_skills else [],
        }

        # Generate and validate section summary
        summary = generate_section_summary("Role Information", str(st.session_state.role_info))
        st.session_state.role_info_summary = summary
        st.write("Summary:", summary)
        change_page(1)

def benefits_page():
    st.title("Benefits")
    benefits = st.text_area("List of Benefits:")

    if st.button("Next"):
        if not benefits:
            st.error("Please provide the benefits.")
            return

        st.session_state.benefits = benefits

        # Generate and validate section summary
        summary = generate_section_summary("Benefits", benefits)
        st.session_state.benefits_summary = summary
        st.write("Summary:", summary)
        change_page(1)

def recruitment_process_page():
    st.title("Recruitment Process")
    recruitment_process = st.text_area("Describe the Recruitment Process:")

    if st.button("Next"):
        if not recruitment_process:
            st.error("Please describe the recruitment process.")
            return

        st.session_state.recruitment_process = recruitment_process

        # Generate and validate section summary
        summary = generate_section_summary("Recruitment Process", recruitment_process)
        st.session_state.recruitment_process_summary = summary
        st.write("Summary:", summary)
        change_page(1)

def job_ad_page():
    st.title("Generated Job Advertisement")
    if all(key in st.session_state for key in ["company_info", "role_info", "benefits", "recruitment_process"]):
        job_ad = generate_job_advertisement(
            company_info=str(st.session_state.company_info_summary),
            role_info=str(st.session_state.role_info_summary),
            benefits=str(st.session_state.benefits_summary),
            recruitment_process=str(st.session_state.recruitment_process_summary),
        )
        st.write("Job Advertisement:")
        st.write(job_ad)
        st.download_button("Download Job Advertisement", job_ad, file_name="job_advertisement.txt")
    else:
        st.error("Incomplete information. Please fill out all sections.")

# Page Mapping
pages = {
    1: company_info_page,
    2: role_info_page,
    3: benefits_page,
    4: recruitment_process_page,
    5: job_ad_page,
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
