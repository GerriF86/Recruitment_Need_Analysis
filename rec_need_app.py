# rec_need_app.py
import streamlit as st
from multiapp import MultiApp
from pages.Recruiting_App import recruiting_app_content
from pages.Impressum import impressum_content
from pages.Our_Mission import our_mission_content
from pages.About_Us import about_us_content
from helpers.utils import sanitize_input

# Instantiate the MultiApp class
app = MultiApp()

# Register the pages
app.add_app("Recruiting App", recruiting_app_content)
app.add_app("Our Mission", our_mission_content)
app.add_app("About Us", about_us_content)
app.add_app("Impressum", impressum_content)

# Run the app
app.run()

# Additional example: sanitizing user input before processing it
input_text = st.text_input("Enter some data")
sanitized_input = sanitize_input(input_text)
st.write(f"Sanitized Input: {sanitized_input}")
