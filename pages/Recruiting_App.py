import streamlit as st
from utils import generate_role_skills, generate_section_summary, generate_job_advertisement

# Page configuration
st.set_page_config(page_title="Recruitment Need Analysis", page_icon="📄", layout="wide")

# Navigation State
if "page" not in st.session_state:
    st.session_state.page = 1

# Navigation Functionality
def next_page():
    st.session_state.page += 1

def previous_page():
    st.session_state.page -= 1

# Company Information Section
if st.session_state.page == 1:
    st.title("Company Information")
    company_name = st.text_input("Company Name:")
    location = st.text_input("Location:")
    work_model = st.selectbox("Work Model:", ["Onsite", "Remote", "Hybrid"])

    # Dynamic questions for hybrid work model
    if work_model == "Hybrid":
        hybrid_ratio = st.slider("Percentage Onsite/Remote:", 0, 100, (50, 50))

    industry = st.text_input("Industry:")
    company_size = st.number_input("Company Size (Number of Employees):", min_value=1, step=1)

    # Save details and move to next page
    if st.button("Next"):
        st.session_state.company_info = {
            "name": company_name,
            "location": location,
            "work_model": work_model,
            "hybrid_ratio": hybrid_ratio if work_model == "Hybrid" else None,
            "industry": industry,
            "company_size": company_size
        }
        next_page()

# Role Information Section
elif st.session_state.page == 2:
    st.title("Role Information")
    role = st.text_input("Role Title:")
    must_have_skills = st.multiselect("Must-Have Skills:", generate_role_skills(role))
    nice_to_have_skills = st.multiselect("Nice-to-Have Skills:", generate_role_skills(role))

    # Save details and move to next page
    if st.button("Next"):
        st.session_state.role_info = {
            "role": role,
            "must_have_skills": must_have_skills,
            "nice_to_have_skills": nice_to_have_skills
        }
        next_page()

    if st.button("Back"):
        previous_page()

# Benefits Section
elif st.session_state.page == 3:
    st.title("Benefits")
    benefits = st.text_area("List the benefits offered to employees:")

    # Save details and move to next page
    if st.button("Next"):
        st.session_state.benefits = benefits
        next_page()

    if st.button("Back"):
        previous_page()

# Recruitment Process Section
elif st.session_state.page == 4:
    st.title("Recruitment Process")
    recruitment_process = st.text_area("Describe the recruitment process:")

    # Save details and move to next page
    if st.button("Next"):
        st.session_state.recruitment_process = recruitment_process
        next_page()

    if st.button("Back"):
        previous_page()

# Job Advertisement Summary
elif st.session_state.page == 5:
    st.title("Job Advertisement")

    # Generate summary and job ad
    company_summary = generate_section_summary("Company Info", st.session_state.company_info)
    role_summary = generate_section_summary("Role Info", st.session_state.role_info)
    benefits_summary = generate_section_summary("Benefits", st.session_state.benefits)
    recruitment_summary = generate_section_summary("Recruitment Process", st.session_state.recruitment_process)
    job_ad = generate_job_advertisement(
        company_summary, role_summary, benefits_summary, recruitment_summary
    )

    st.subheader("Generated Job Advertisement")
    st.write(job_ad)

    if st.button("Back"):
        previous_page()

# Footer
st.markdown("---")
st.caption("Recruitment Need Analysis Tool powered by AI.")
