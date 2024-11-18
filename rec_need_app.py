import streamlit as st
from multiapp import MultiApp
from pages.Recruiting_App import recruiting_app_content
from pages.Impressum import impressum_content
from pages.Our_Mission import our_mission_content
from pages.About_Us import about_us_content

# Instantiate the MultiApp class
app = MultiApp()

# Register the pages
app.add_app("Recruiting App", recruiting_app_content)
app.add_app("Our Mission", our_mission_content)
app.add_app("About Us", about_us_content)
app.add_app("Impressum", impressum_content)

# Hide Streamlit's default navigation and footer
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    app.run()
