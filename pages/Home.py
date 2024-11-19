import streamlit as st
from rec_need_app import home_page

# Set page configuration
st.set_page_config(page_title="Home - Recruitment Need Analysis", page_icon="🏠", layout="wide")

# Render the Home page
home_page()
