# main_rec_need_app.py

import streamlit as st
from pages.Impressum import impressum_content
from pages.Our_Mission import mission_content
from pages.Recruiting_App import recruiting_app_content
from pages.About_Us import about_us_content

# Page navigation options
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Recruiting App", "Our Mission", "About Us", "Impressum"])

# Page display logic
if page == "Recruiting App":
    recruiting_app_content()
elif page == "Our Mission":
    mission_content()
elif page == "About Us":
    about_us_content()
elif page == "Impressum":
    impressum_content()

# Functionality for Recruiting_App (integrating previous pages like Job Description, Skills, Benefits, Summary)
# This function would now be inside 'pages/Recruiting_App.py' to make it a unified content handler.
