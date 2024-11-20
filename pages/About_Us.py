import streamlit as st

def about_us_page():
    st.title("About Us")
    st.markdown("""
    ### Revolutionizing Recruitment Through AI
    Our app leverages state-of-the-art AI technologies to enhance recruitment workflows, making hiring smarter, faster, and more effective.
    """)

# Set page configuration
st.set_page_config(page_title="About Us", page_icon="ℹ️", layout="wide")

# Render the About Us page
about_us_page()
