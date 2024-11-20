import streamlit as st
import toml
from pathlib import Path
import sys
from helpers.utils import (
    validate_job_title,
    cached_generate_role_skills,
    generate_job_advertisement,
    change_page,
    query_local_llm
)

# Load configurations from config.toml
config = toml.load("config.toml")

# Dynamically add the project root to the Python path to fix import issues
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Set page configuration - use settings from config.toml
st.set_page_config(
    page_title=config["app"]["page_title"],
    page_icon=config["app"]["page_icon"],
    layout=config["app"].get("layout", "wide")
)

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

    # Updated slider for Number of Employees
    company_size = st.slider(
        "Number of Employees:",
        min_value=1,
        max_value=1000,
        value=200,  # Default value
        step=10,  # Step size
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

        summary = f"Company Information Summary:\nCompany Name: {company_name}\nLocation: {location}\nIndustry: {industry}\nCompany Size: {company_size}"
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
        # Use cached_generate_role_skills
        skills_categories = cached_generate_role_skills(role)
        skills = [skill for category in skills_categories.values() for skill in category]
        
        if skills:
            st.markdown("### Suggested Skills:")
            for skill in skills:
                st.write(f"- {skill}")

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

        summary = (
            f"Role Information Summary:\n"
            f"Role Title: {role}\n"
            f"Must-Have Skills: {', '.join(must_have_skills.split(','))}\n"
            f"Nice-to-Have Skills: {', '.join(nice_to_have_skills.split(','))}"
        )
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
        summary = f"Benefits Summary:\n{benefits}"
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
        summary = f"Recruitment Process Summary:\n{recruitment_process}"
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
