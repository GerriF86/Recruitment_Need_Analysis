# pages/Impressum.py
import streamlit as st
import os

def impressum_content():
    # Load the HTML template for Impressum
    with open(os.path.join("templates", "Impressum.html"), "r") as html_file:
        html_content = html_file.read()

    # Render the HTML template in Streamlit
    st.components.v1.html(html_content, height=600)
