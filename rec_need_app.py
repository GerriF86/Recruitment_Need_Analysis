import streamlit as st
from pathlib import Path
import sys
from dotenv import load_dotenv
import os
from helpers.utils import (
   # format_response,
    #extract_keywords_from_text,
    load_html_template,
    custom_css,
    top_navbar,
    home_page,
    about_us_page,
    our_mission_page,
    magic_behind_the_scenes_page,
    impressum_page,
)

# Load environment variables
load_dotenv()
groq_key = os.getenv("groq_key")

# Ensure proper imports
sys.path.append(str(Path(__file__).resolve().parent.parent))

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
