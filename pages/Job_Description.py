import streamlit as st
from pages.Role_Benefits import app as role_benefits_app


def app():
    st.title("Job Description Generator")

    role_input = st.text_input("Enter the role you're hiring for:", placeholder="E.g., Data Scientist")

    # Generate job description
    if st.button("Generate Job Description"):
        if role_input:
            job_description = get_suggestions(f"Generate a job description for a {role_input}")
            st.session_state['job_description'] = job_description
        else:
            st.warning("Please enter a role to generate a job description.")

    # Display generated job description
    if 'job_description' in st.session_state:
        st.text_area("Generated Job Description:", value="\n".join(st.session_state['job_description']), height=300)

    # Navigation to the next section
    if st.button("Next"):
        st.session_state['navigate_to'] = 'Role_Benefits'