import streamlit as st
from pathlib import Path
import sys
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
groq_key = os.getenv("groq_key")

# Ensure proper imports
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Import from helpers directory
from helpers.state_management import cached_generate_role_skills, change_page  # State management functions
from helpers.llm_utils import query_local_llm, query_remote_api, query_rag  # LLM-related functions
from helpers.utils import format_response, extract_keywords_from_text, load_html_template  # General utilities

# Custom CSS for styling
def custom_css():
    st.markdown("""
        <style>
        body { background-color: #1f1f1f; color: #ffffff; font-family: 'Roboto', sans-serif; }
        h1, h2, h3 { color: #00d4ff; text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.8); }
        .stButton>button { background: linear-gradient(90deg, #007cf0, #00dfd8); color: white; font-size: 18px; border-radius: 8px; padding: 10px 20px; }
        .top-navbar { display: flex; justify-content: space-around; background-color: #444; padding: 1em; }
        .nav-link { color: #fff; text-decoration: none; font-weight: bold; padding: 0.5em; transition: background 0.3s; }
        .nav-link:hover { background-color: #555; }
        footer {visibility: hidden;}
        #MainMenu {visibility: hidden;}
        .button-wrapper { display: flex; justify-content: center; margin-top: 2em; }
        </style>
    """, unsafe_allow_html=True)

# Top navigation bar component
def top_navbar():
    st.markdown("""
        <div class="top-navbar">
            <a href="/Home" class="nav-link">Home</a>
            <a href="/About_Us" class="nav-link">About Us</a>
            <a href="/Our_Mission" class="nav-link">Our Mission</a>
            <a href="/The_Magic_behind_the_Scenes" class="nav-link">The Magic Behind the Scenes</a>
            <a href="/Impressum" class="nav-link">Impressum</a>
        </div>
    """, unsafe_allow_html=True)

# Page Functions Defined Here
def home_page():
    st.title("Welcome to the Recruitment Revolution")
    st.markdown("""
        ### Your Ultimate Hiring Companion
        Harness the power of cutting-edge AI to revolutionize the way you hire.
        Navigate to any section from the navigation bar at the top to begin.
    """)
    
    # Use placeholder or fix the path of the local image
    st.image("https://via.placeholder.com/800x400", caption="Streamline Your Recruitment Process", use_container_width=True)

    # Highlighted button for Recruitment Need Analysis prominently in the center
    st.markdown('<div class="button-wrapper">', unsafe_allow_html=True)
    if st.button("Start Recruitment Need Analysis", key="highlighted_button"):
        st.query_params.update({"page": "Recruiting_App"})  # Updated to st.query_params
    st.markdown('</div>', unsafe_allow_html=True)

def about_us_page():
    st.title("About Us")
    st.markdown("""
        ### Revolutionizing Recruitment Through AI
        Our app leverages **Llama**, a large language model trained on millions of job-related data points, to understand recruitment like never before.
    """)

def our_mission_page():
    st.title("Our Mission")
    st.markdown("""
        ### Changing Recruitment for Good
        Our mission is to empower businesses with a recruitment tool that combines state-of-the-art AI and intuitive design to make hiring smarter.
    """)

def magic_behind_the_scenes_page():
    st.title("The Magic Behind the Scenes")
    st.markdown("""
        ### Cutting-Edge Recruitment Technology
        Powered by **local large language models**, **state machines**, and **graph databases**.
    """)

def impressum_page():
    st.title("Impressum")
    st.markdown("""
        ### Legal Information
        All rights reserved. Unauthorized use is prohibited.
    """)

# Main app logic
def main():
    # Apply custom CSS
    custom_css()
    top_navbar()

    # Extracting page from URL
    page_url = st.query_params.get("page", ["Home"])[0]

    # Directly rendering the page based on the current URL path
    if page_url == "Home":
        home_page()
    elif page_url == "About_Us":
        about_us_page()
    elif page_url == "Our_Mission":
        our_mission_page()
    elif page_url == "The_Magic_behind_the_Scenes":
        magic_behind_the_scenes_page()
    elif page_url == "Impressum":
        impressum_page()

if __name__ == "__main__":
    main()
