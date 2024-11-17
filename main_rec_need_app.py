import streamlit as st
from streamlit_option_menu import option_menu
from pages.blick_unter_motorhaube import blick_unter_die_motorhaube
from pages.about_us import about_us
from pages.home_page import load_home_page
from pages.recruitment_page import recruitment_page
from pages.impressum_page import load_impressum_page

# Main function to manage navigation between pages
def main():
    # Sidebar menu for navigation
    with st.sidebar:
        selected = option_menu(
            menu_title="Main Menu",  # Required
            options=["Home", "Blick unter die Motorhaube", "About Us", "Recruitment Need Analysis", "Impressum"],  # Menu options
            icons=["house", "wrench", "info-circle", "briefcase", "file-alt"],  # Icons for each page
            menu_icon="cast",  # Icon for the menu
            default_index=0,  # Default selected page
            styles={
                "container": {"padding": "5px", "background-color": "#f0f0f0"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "5px",
                    "--hover-color": "#eee"
                },
                "icon": {"color": "blue", "font-size": "20px"},
            },
        )
    
    # Page selection logic
    if selected == "Blick unter die Motorhaube":
        blick_unter_die_motorhaube()
    elif selected == "About Us":
        about_us()
    elif selected == "Recruitment Need Analysis":
        recruitment_page()
    elif selected == "Impressum":
        load_impressum_page()
    else:
        load_home_page()

# Run the main function
if __name__ == "__main__":
    main()