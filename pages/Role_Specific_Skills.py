import streamlit as st
from utils.utility import fetch_from_llama

def app():
    st.title("Role-Specific Skills Suggestions")

    role_input = st.text_input("Enter the role you're hiring for:", placeholder="E.g., Python Developer")

    # Generate suggestions
    if st.button("Get Skills Suggestions"):
        if role_input:
            skills = fetch_from_llama(f"Suggest technical skills for a {role_input}")
            st.session_state['skills'] = skills
        else:
            st.warning("Please enter a role to generate skills.")