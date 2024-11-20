import streamlit as st
import toml
import re
from pathlib import Path
import sys
from helpers.utils import (
    validate_job_title,
    cached_generate_role_skills,
    generate_job_advertisement,
    #query_local_llm,
    cached_generate_role_benefits,
    cached_generate_role_recruitment_steps,
    change_page
)

# Load configurations from config.toml
try:
    config = toml.load("config.toml")
except Exception as e:
    st.error(f"Error loading configuration file: {e}")
    st.stop()

# Dynamically add the project root to the Python path to fix import issues
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Set page configuration - use settings from config.toml
st.set_page_config(
    page_title=config["app"]["page_title"],
    page_icon=config["app"]["page_icon"],
    layout=config["app"].get("layout", "wide")
)

# Initialize Session State
session_keys = ["page", "company_info", "role_info", "benefits", "recruitment_process", "must_have_skills", "nice_to_have_skills", "selected_benefits", "selected_recruitment_steps"]
for key in session_keys:
    if key not in st.session_state:
        st.session_state[key] = [] if key in ["must_have_skills", "nice_to_have_skills", "selected_benefits", "selected_recruitment_steps"] else None

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
    role = st.text_input("Role Title:")

    if role and not validate_job_title(role):
        st.error("Invalid role title. Please enter a valid one.")
        return

    if role:
        st.write("Role-Specific Skill Suggestions:")
        skills_categories = cached_generate_role_skills(role)

        # Display categorized skills
        all_skills = {}
        st.markdown("### Suggested Skills:")
        
        for category, skills in skills_categories.items():
            st.subheader(f"{category} Skills")
            all_skills[category] = skills

        # Flatten skills into a single list for user selection
        all_skill_list = [skill for skills in all_skills.values() for skill in skills]

        # Must-Have Skills Selection
        st.markdown("### Select Must-Have Skills")
        must_have_selection = st.multiselect(
            "Select Must-Have Skills:",
            options=all_skill_list,
            default=st.session_state.must_have_skills,
            key="must_have_select"
        )

        # Nice-to-Have Skills Selection
        st.markdown("### Select Nice-to-Have Skills")
        nice_to_have_selection = st.multiselect(
            "Select Nice-to-Have Skills:",
            options=all_skill_list,
            default=st.session_state.nice_to_have_skills,
            key="nice_to_have_select"
        )

        # Update session state
        st.session_state.must_have_skills = must_have_selection
        st.session_state.nice_to_have_skills = nice_to_have_selection

    if st.button("Next"):
        if not role or not st.session_state.must_have_skills:
            st.error("Please provide the role and select must-have skills.")
            return

        st.session_state.role_info = {
            "role": role,
            "must_have_skills": st.session_state.must_have_skills,
            "nice_to_have_skills": st.session_state.nice_to_have_skills,
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
        for benefit in benefits_suggestions:
            st.write(f"- {benefit}")

        # Benefits Selection
        selected_benefits = st.multiselect(
            "Select Benefits for this role:",
            options=benefits_suggestions,
            default=st.session_state.selected_benefits,
            key="benefits_select"
        )

        # Update session state
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
        for step in recruitment_steps_suggestions:
            st.write(f"- {step}")

        # Recruitment Process Selection
        selected_steps = st.multiselect(
            "Select Recruitment Steps for this role:",
            options=recruitment_steps_suggestions,
            default=st.session_state.selected_recruitment_steps,
            key="recruitment_steps_select"
        )

        # Update session state
        st.session_state.selected_recruitment_steps = selected_steps

    additional_steps = st.text_area("Enter any additional recruitment steps you wish to add:")

    if st.button("Next"):
        if not selected_steps and not additional_steps:
            st.error("Please select or enter recruitment steps.")
            return

        st.session_state.recruitment_process = selected_steps + additional_steps.split(",")
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
