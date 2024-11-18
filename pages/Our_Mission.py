# pages/Our_Mission.py
import streamlit as st
import os

def mission_content():
    # Load the HTML template
    with open(os.path.join("templates", "our_mission.html"), "r") as html_file:
        html_content = html_file.read()

    # Render the HTML template in Streamlit
    st.components.v1.html(html_content, height=600)
