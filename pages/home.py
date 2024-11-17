import streamlit as st
import requests
from PIL import Image
import json
import folium
from streamlit_folium import st_folium

def load_home_page():
    # Add an Image above the Header
    try:
        image = Image.open('imgs/iceberg.jpg')
        st.image(image, caption="AI-Powered Job Ad Generator", use_column_width=True)
    except FileNotFoundError:
        st.warning("Image not found. Please ensure the file path is correct.")
    
    # App Title
    st.title("Recruitment Need Analysis App")
    st.subheader("Discover important aspects of the role you want to fill and identify the skills and qualifications you need.")
    
    # Introduction
    st.markdown("""
        Welcome! This app helps you create job descriptions effortlessly by guiding you step-by-step. Whether you're an HR professional or a hiring manager, 
        simply answer the questions and watch the app generate a complete, customized job description tailored to your needs.
    """)