import streamlit as st 
from pages import home, about, impressum

# Page Configuration
st.set_page_config(page_title="AI-Powered Job Ad Generator", page_icon="📄", layout="wide")

# Sidebar for Navigation
st.sidebar.title("")
selected_page = st.sidebar.radio("Go to", ["Home","Recruitment-Need Analyser", "About Us", "Impressum"])

# Page Routing
if selected_page == "Home":
    home.load_home_page()
    elif selected_page == "Recruitment-Need Analyser":
    about.load_Recruitment-Need Analyser_page()
elif selected_page == "About Us":
    about.load_about_page()
elif selected_page == "Impressum":
    impressum.load_impressum_page()