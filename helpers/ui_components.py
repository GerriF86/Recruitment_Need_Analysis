import streamlit as st
from typing import List, Dict
from helpers.state_management import change_page
from helpers.llm_utils import generate_section_summary, generate_job_advertisement
from helpers.utils import cached_generate_role_skills

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

# Page Components
def company_info_page():
    render_header()
    st.header("Company Information")

    company_name = st.text_input("Company Name:")
    location = st.text_input("Location:")
    work_model = st.selectbox("Work Model:", ["Onsite", "Remote", "Hybrid"])
    hybrid_ratio = (
        st.slider("Number of days at home (0-5):", 0, 5, 2),
        st.slider("Number of days in the office (0-5):", 0, 5, 3)
    ) if work_model == "Hybrid" else None
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
        skills = cached_generate_role_skills(role)
        categories = categorize_skills(skills)
        
        st.subheader("Categorized Skills")
        for category, skills in categories.items():
            st.write(f"**{category}:**")
            st.write(", ".join(skills))
        
        must_have_skills = st.multiselect("Must-Have Skills:", [skill for skill_list in categories.values() for skill in skill_list])
        nice_to_have_skills = st.multiselect("Nice-to-Have Skills:", [skill for skill_list in categories.values() for skill in skill_list])
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

def categorize_skills(skills: List[str]) -> Dict[str, List[str]]:
    categories = {"Technical Skills": [], "Soft Skills": [], "Management Skills": [], "Industry Knowledge": [], "Miscellaneous": []}
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

def summary_page():
    render_header()
    st.header("Summary of Entered Information")

    st.subheader("Company Information")
    st.write(st.session_state.get("company_info", "Not provided"))

    st.subheader("Role Information")
    st.write(st.session_state.get("role_info", "Not provided"))

    st.subheader("Benefits and Compensation")
    st.write(st.session_state.get("benefits", "Not provided"))

    st.subheader("Recruitment Process")
    st.write(st.session_state.get("recruitment_process", "Not provided"))

    st.markdown("---")
    st.warning("Please review the information above. If there are any mistakes, navigate back to make adjustments.")

    if st.button("Generate Job Advertisement"):
        if all([st.session_state.get("company_info"), st.session_state.get("role_info"), st.session_state.get("benefits"), st.session_state.get("recruitment_process")]):
            change_page(1)
        else:
            st.error("Please ensure all sections are completed before proceeding.")

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
