import streamlit as st

def app():
    st.title("Welcome to the Home Page")
    st.markdown("""
    ### Overview
    Welcome to the Recruitment Need Analysis Web App! Here you can explore various features:
    
    - Perform a **Recruiting Need Analysis**.
    - Identify **Role-Specific Skills**.
    - Create targeted **Job Descriptions**.
    - Discover potential **Role Benefits**.
    - View a comprehensive **Summary** of your selections.
    - Learn more about **Our Mission**.

    Navigate through the menu to get started!
    """)
    st.image("static/home_banner.jpg", caption="Recruitment Simplified", use_column_width=True)
