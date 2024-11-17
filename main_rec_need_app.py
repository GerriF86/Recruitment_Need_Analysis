import streamlit as st
from multiapp import MultiApp

# Import each page
from pages.Recruiting_App import recruiting_app
from pages.Role_Specific_Skills import app as role_skills_app
from pages.Job_Description import app as job_desc_app
from pages.Role_Benefits import app as role_benefits_app
from pages.Summary import app as summary_app
from pages.Our_Mission import app as our_mission_app
#from pages.about_us import app as about_us_app
#from pages.Impressum import app as impressum_app

# Initialize session state for navigation
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'home'

# Page navigation mapping
PAGES = {
    "home": lambda: st.write("Welcome to the Home Page!"),
    "recruiting": recruiting_app,
    "role_skills": role_skills_app,
    "job_description": job_desc_app,
    "role_benefits": role_benefits_app,
    "summary": summary_app,
    "our_mission": our_mission_app,
    #"about_us": about_us_app,
    #"impressum": impressum_app,
}

# Render current page
PAGES[st.session_state['current_page']]()

# Helper function for page navigation
def navigate_to(page_key):
    st.session_state['current_page'] = page_key