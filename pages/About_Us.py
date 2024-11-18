# pages/About_Us.py
import streamlit as st
import os

def about_us_content():
    # Load the HTML template
    with open(os.path.join("templates", "about_us.html"), "r") as html_file:
        html_content = html_file.read()

    # Render the HTML template in Streamlit
    st.components.v1.html(html_content, height=600)
