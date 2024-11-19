import streamlit as st
import os

def impressum_content():
    try:
        # Load the HTML template for Impressum
        with open(os.path.join("templates", "Impressum.html"), "r") as html_file:
            html_content = html_file.read()

        # Render the HTML template in Streamlit
        st.components.v1.html(html_content, height=600)
    except FileNotFoundError:
        st.error("Impressum.html template not found. Please ensure the file is located in the 'templates' directory.")