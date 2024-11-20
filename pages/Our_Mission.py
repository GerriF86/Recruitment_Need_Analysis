import streamlit as st

def our_mission_page():
    st.title("Our Mission")
    st.markdown("""
    ### Empowering Recruitment for the Future
    Our mission is to provide businesses with tools that streamline the hiring process while improving the candidate experience.
    """)

# Set page configuration
st.set_page_config(page_title="Our Mission", page_icon="🎯", layout="wide")

# Render the Our Mission page
our_mission_page()
