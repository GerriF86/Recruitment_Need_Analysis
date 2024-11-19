import streamlit as st
from helpers.utils import (
    validate_job_title,
    format_response,
    extract_keywords_from_text,
    load_html_template,
    query_local_llm,
    generate_role_skills,
    generate_section_summary,
    generate_job_advertisement,
)

# Custom CSS for styling
def custom_css():
    st.markdown("""
        <style>
        body { background-color: #1f1f1f; color: #ffffff; font-family: 'Roboto', sans-serif; }
        h1, h2, h3 { color: #00d4ff; text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.8); }
        .stButton>button { background: linear-gradient(90deg, #007cf0, #00dfd8); color: white; font-size: 18px; border-radius: 8px; padding: 10px 20px; }
        footer {visibility: hidden;}
        #MainMenu {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

# Define pages as individual functions
def home_page():
    st.title("Welcome to the Recruitment Revolution")
    st.markdown("""
        ### Your Ultimate Hiring Companion
        Harness the power of cutting-edge AI to revolutionize the way you hire.
        Navigate to any section from the sidebar to begin.
    """)
    st.image("https://via.placeholder.com/800x400", caption="Streamline Your Recruitment Process")

def about_us_page():
    st.title("About Us")
    st.markdown("""
        ### Revolutionizing Recruitment Through AI
        Our app leverages **Llama**, a large language model trained on millions of job-related data points, to understand recruitment like never before.
    """)

def our_mission_page():
    st.title("Our Mission")
    st.markdown("""
        ### Changing Recruitment for Good
        Our mission is to empower businesses with a recruitment tool that combines state-of-the-art AI and intuitive design to make hiring smarter.
    """)

def need_analysis_page():
    st.title("Need Analysis")
    st.markdown("Enter detailed role and organizational information to generate a tailored job ad.")
    company_name = st.text_input("Company Name:")
    role = st.text_input("Role Title:")
    if role:
        skills = generate_role_skills(role)
        st.multiselect("Must-Have Skills:", skills)
        st.multiselect("Nice-to-Have Skills:", skills)

def impressum_page():
    st.title("Impressum")
    st.markdown("""
        ### Legal Information
        All rights reserved. Unauthorized use is prohibited.
    """)

def magic_behind_the_scenes_page():
    st.title("The Magic Behind the Scenes")
    st.markdown("""
        ### Cutting-Edge Recruitment Technology
        Powered by **local large language models**, **state machines**, and **graph databases**.
    """)

# Main app logic
def main():
    custom_css()

    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to:",
        ["Home", "About Us", "Our Mission", "Need Analysis", "Impressum", "The Magic Behind the Scenes"]
    )

    # Page rendering logic
    if page == "Home":
        home_page()
    elif page == "About Us":
        about_us_page()
    elif page == "Our Mission":
        our_mission_page()
    elif page == "Need Analysis":
        need_analysis_page()
    elif page == "Impressum":
        impressum_page()
    elif page == "The Magic Behind the Scenes":
        magic_behind_the_scenes_page()

# Run the app
if __name__ == "__main__":
    main()
