import streamlit as st
from streamlit_option_menu import option_menu
from blick_unter_motorhaube import blick_unter_die_motorhaube
from about_us import about_us

# Main function to manage navigation between pages
def main():
    # Sidebar menu for navigation
    with st.sidebar:
        selected = option_menu(
            menu_title="Main Menu",  # Required
            options=["Home", "Blick unter die Motorhaube", "About Us"],  # Menu options
            icons=["house", "wrench", "info-circle"],  # Icons for each page
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
    else:
        st.title("Home Page")
        st.write("Welcome to the Home Page! Use the sidebar to navigate through the app.")

# Run the main function
if __name__ == "__main__":
    main()