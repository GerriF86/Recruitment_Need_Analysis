import streamlit as st
import os

def about_us_content():
    try:
        # Load the HTML template for About Us
        with open(os.path.join("templates", "about_us.html"), "r") as html_file:
            html_content = html_file.read()

        # Render the HTML template in Streamlit
        st.components.v1.html(html_content, height=600)
    except FileNotFoundError:
        st.error("About Us template not found. Please ensure the file is located in the 'templates' directory.")
