import streamlit as st

def impressum_page():
    st.title("Impressum")
    st.markdown("""
    ### Legal Information
    All rights reserved. Unauthorized use is prohibited.
    """)

# Set page configuration
st.set_page_config(page_title="Impressum", page_icon="📜", layout="wide")

# Render the Impressum page
impressum_page()
