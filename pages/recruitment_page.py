import streamlit as st
import folium
from streamlit_folium import st_folium

def recruitment_page():
    # Job Title Input
    st.header("Job Title")
    job_title = st.text_input("Enter the Job Title:")
    
    if st.button("Next") and job_title:
        st.session_state['job_title'] = job_title
        load_company_details()


def load_company_details():
    st.sidebar.header("Summary of Inputs")
    st.sidebar.write(f"**Job Title:** {st.session_state.get('job_title', '')}")

    # Step 2: Company Details
    st.header("Company Details")
    company = st.text_input("Enter the Company Name:")
    email = st.text_input("Enter the Contact Email to be Published on Job Ad:")
    place_of_work = st.text_input("Enter the Place of Work:")
    start_date = st.date_input("Select the Start Date:")
    employment_type = st.selectbox("Select Employment Type:", ["Full-Time", "Part-Time", "Contract", "Temporary"])
    
    # Display Place of Work on OpenStreetMap
    if place_of_work:
        location_map = folium.Map(location=[50.1109, 8.6821], zoom_start=12)
        folium.Marker([50.1109, 8.6821], popup=place_of_work).add_to(location_map)
        st_folium(location_map, width=700, height=500)

    if st.button("Next - Responsibilities") and company and email and place_of_work:
        st.session_state.update({
            'company': company, 'email': email,
            'place_of_work': place_of_work, 'start_date': start_date,
            'employment_type': employment_type
        })
        load_responsibilities()


def load_responsibilities():
    st.header("Role-Specific Responsibilities")
    suggested_responsibilities = [
        "Develop machine learning models",
        "Analyze large datasets",
        "Collaborate with cross-functional teams",
        "Create detailed reports"
    ]
    selected_responsibilities = st.multiselect("Select Suitable Responsibilities:", suggested_responsibilities)
    additional_responsibilities = st.text_area("Enter Additional Responsibilities (if any):")

    if st.button("Next - Requirements"):
        st.session_state['responsibilities'] = selected_responsibilities + [additional_responsibilities]
        load_requirements()


def load_requirements():
    st.header("Role-Specific Requirements")
    suggested_requirements = [
        "Bachelor's degree in Computer Science or related field",
        "3+ years of experience in data analysis",
        "Proficiency in Python and SQL",
        "Strong problem-solving skills"
    ]
    selected_requirements = st.multiselect("Select Suitable Requirements:", suggested_requirements)
    additional_requirements = st.text_area("Enter Additional Requirements (if any):")

    if st.button("Next - Benefits"):
        st.session_state['requirements'] = selected_requirements + [additional_requirements]
        load_benefits()


def load_benefits():
    st.header("Benefits")
    suggested_benefits = [
        "Health insurance",
        "Flexible working hours",
        "Remote work options",
        "Professional development opportunities"
    ]
    selected_benefits = st.multiselect("Select Suitable Benefits:", suggested_benefits)
    additional_benefits = st.text_area("Enter Additional Benefits (if any):")

    if st.button("Generate Job Advertisement"):
        st.session_state['benefits'] = selected_benefits + [additional_benefits]