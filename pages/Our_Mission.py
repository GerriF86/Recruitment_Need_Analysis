import streamlit as st
import os

def our_mission_content():
    try:
        # Load the HTML template for Our Mission
        with open(os.path.join("templates", "our_mission.html"), "r") as html_file:
            html_content = html_file.read()

        # Render the HTML template in Streamlit
        st.components.v1.html(html_content, height=600)
    except FileNotFoundError:
        st.error("Our Mission template not found. Please ensure the file is located in the 'templates' directory.")
