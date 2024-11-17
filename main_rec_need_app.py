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

# All pages with their corresponding keys and functions
ALL_PAGES = {
    "home": lambda: st.write("Welcome to the Home Page!"),
    "recruiting": recruiting_app,
    "role_skills": role_skills_app,
    "job_description": job_desc_app,
    "role_benefits": role_benefits_app,
    "summary": summary_app,
    "our_mission": our_mission_app,
    "about_us": about_us_app,
    "impressum": impressum_app,
}

# Define the visible pages and their order
visible_pages = [
    ("home", "Home"),
    ("recruiting", "Recruiting App"),

    # Add or remove pages from this list as needed
]

# Create a navigation menu in the sidebar or at the top
st.sidebar.title("Navigation")
selected_page = st.sidebar.radio(
    "Go to:",
    options=[page[1] for page in visible_pages],
    index=[page[0] for page in visible_pages].index(st.session_state['current_page']),
)

# Update session state based on user selection
for key, name in visible_pages:
    if name == selected_page:
        st.session_state['current_page'] = key

# Render the selected page
ALL_PAGES[st.session_state['current_page']]()
