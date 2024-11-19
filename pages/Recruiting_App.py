import streamlit as st
import sys
from pathlib import Path
from helpers.utils import validate_job_title, format_response, extract_keywords_from_text, load_html_template, query_local_llm, generate_role_skills, generate_section_summary, generate_job_advertisement


# Dynamically add the project root to the Python path to fix import issues
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Safely import utils with error handling
try:
    from helpers.utils import (
        generate_role_skills,
        generate_section_summary,
        generate_job_advertisement,
    )
except ImportError as e:
    st.error(f"Error loading helpers: {e}")
    st.stop()

# Page Configuration
st.set_page_config(
    page_title="Recruitment Need Analysis",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Initialize Session State
session_keys = ["page", "company_info", "role_info", "benefits", "recruitment_process"]
for key in session_keys:
    st.session_state.setdefault(key, 1 if key == "page" else None)

# Navigation Functions
def change_page(step: int):
    st.session_state.page += step

# Common Header
def render_header():
    st.title("Recruitment Need Analysis Tool")
    st.markdown("""
        ### How It Works
        1. Enter the role name (e.g., "Data Analyst") into our app.
        2. Engage in an intuitive question-and-answer flow tailored to your organizational structure.
        3. Receive a complete, structured summary of the role, ready to create targeted job ads or guide recruitment strategies.
        ---
    """)

# Caching Skill Generation for Performance
@st.cache_data
def cached_generate_role_skills(role):
    return generate_role_skills(role)

# Page Components
def company_info_page():
    render_header()
    st.header("Company Information")

    company_name = st.text_input("Company Name:")
    location = st.text_input("Location:")
    work_model = st.selectbox("Work Model:", ["Onsite", "Remote", "Hybrid"])
    hybrid_ratio = (
        st.slider("Percentage Onsite/Remote:", 0, 100, (50, 50)) if work_model == "Hybrid" else None
    )
    industry = st.text_input("Industry:")
    company_size = st.number_input("Company Size (Number of Employees):", min_value=1, step=1)

    if st.button("Next") and company_name and location and industry:
        st.session_state.company_info = {
            "name": company_name,
            "location": location,
            "work_model": work_model,
            "hybrid_ratio": hybrid_ratio,
            "industry": industry,
            "company_size": company_size,
        }
        change_page(1)

def role_info_page():
    render_header()
    st.header("Role Information")

    role = st.text_input("Role Title:")
    if role:
        must_have_skills = st.multiselect("Must-Have Skills:", cached_generate_role_skills(role))
        nice_to_have_skills = st.multiselect("Nice-to-Have Skills:", cached_generate_role_skills(role))
    else:
        st.warning("Enter a role to generate skills.")

    if st.button("Next") and role:
        st.session_state.role_info = {
            "role": role,
            "must_have_skills": must_have_skills,
            "nice_to_have_skills": nice_to_have_skills,
        }
        change_page(1)

    if st.button("Back"):
        change_page(-1)

def benefits_page():
    render_header()
    st.header("Benefits and Compensation")

    benefits = st.text_area("List the benefits offered to employees:")

    if st.button("Next") and benefits:
        st.session_state.benefits = benefits
        change_page(1)

    if st.button("Back"):
        change_page(-1)

def recruitment_process_page():
    render_header()
    st.header("Recruitment Process")

    recruitment_process = st.text_area("Describe the recruitment process:")

    if st.button("Next") and recruitment_process:
        st.session_state.recruitment_process = recruitment_process
        change_page(1)

    if st.button("Back"):
        change_page(-1)

def job_ad_page():
    render_header()
    st.header("Generated Job Advertisement")

    # Generate summaries and job ad
    company_summary = generate_section_summary("Company Information", st.session_state.get("company_info", {}))
    role_summary = generate_section_summary("Role Information", st.session_state.get("role_info", {}))
    benefits_summary = generate_section_summary("Benefits", st.session_state.get("benefits", ""))
    recruitment_summary = generate_section_summary("Recruitment Process", st.session_state.get("recruitment_process", ""))
    job_ad = generate_job_advertisement(company_summary, role_summary, benefits_summary, recruitment_summary)

    # Display and download the job ad
    st.subheader("Job Advertisement")
    st.write(job_ad)
    st.download_button(
        label="Download Job Advertisement",
        data=job_ad,
        file_name="Job_Advertisement.txt",
        mime="text/plain",
    )

    if st.button("Back"):
        change_page(-1)

# Main App Navigation
def main():
    pages = {
        1: company_info_page,
        2: role_info_page,
        3: benefits_page,
        4: recruitment_process_page,
        5: job_ad_page,
    }

    # Dynamically call the current page function
    current_page = st.session_state.page
    pages.get(current_page, company_info_page)()

if __name__ == "__main__":
    main()

# Footer Styling
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)