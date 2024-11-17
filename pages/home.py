import streamlit as st
import requests
from PIL import Image
import json
import folium
from streamlit_folium import st_folium

def load_home_page():
    # Add an Image above the Header
    try:
        image = Image.open('imgs/iceberg.jpg')
        st.image(image, caption="AI-Powered Job Ad Generator", use_column_width=True)
    except FileNotFoundError:
        st.warning("Image not found. Please ensure the file path is correct.")
    
    # App Title
    st.title("Recruitment Need Analysis App")
    st.subheader("Discover important aspects of the role you want to fill and identify the skills and qualifications you need.")
    
    # Introduction
    st.markdown("""
        This app assists HR professionals in creating comprehensive job descriptions 
        by guiding them through interactive questions. Answer a series of prompts to 
        generate a formatted job description tailored to your needs.
    """)
    
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
        generate_job_ad()

def generate_job_ad():
    st.header("Generated Job Advertisement")
    prompt = f"""
    Create a job advertisement for the following position:

    **Job Title:** {st.session_state['job_title']}
    **Company:** {st.session_state['company']}
    **Location:** {st.session_state['place_of_work']}
    **Start Date:** {st.session_state['start_date']}
    **Employment Type:** {st.session_state['employment_type']}

    **Responsibilities:**
    {', '.join(st.session_state['responsibilities'])}

    **Requirements:**
    {', '.join(st.session_state['requirements'])}

    **Benefits:**
    {', '.join(st.session_state['benefits'])}
    """
    
    try:
        response = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={"model": "koesn/dolphin-llama3-8b", "prompt": prompt, "num_ctx": 8192},
            stream=True
        )   
        response.raise_for_status()

        job_ad = ""
        for line in response.iter_lines():
            if line:
                chunk = line.decode("utf-8")
                data = json.loads(chunk)
                job_ad += data.get("response", "")
                if data.get("done", False):
                    break

        if job_ad.strip():
            st.subheader("Generated Job Advertisement:")
            st.markdown(job_ad)
            st.download_button(
                label="Download Job Advertisement",
                data=job_ad,
                file_name=f"{st.session_state['job_title']}_Job_Ad.txt",
                mime="text/plain"
            )
            st.sidebar.header("Summary of Inputs")
            st.sidebar.write(f"**Job Title:** {st.session_state['job_title']}")
            st.sidebar.write(f"**Company:** {st.session_state['company']}")
            st.sidebar.write(f"**Location:** {st.session_state['place_of_work']}")
            st.sidebar.write(f"**Start Date:** {st.session_state['start_date']}")
            st.sidebar.write(f"**Employment Type:** {st.session_state['employment_type']}")
            st.sidebar.write(f"**Responsibilities:** {', '.join(st.session_state['responsibilities'])}")
            st.sidebar.write(f"**Requirements:** {', '.join(st.session_state['requirements'])}")
            st.sidebar.write(f"**Benefits:** {', '.join(st.session_state['benefits'])}")
        else:
            st.error("The model did not return any content. Please try again.")
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")
