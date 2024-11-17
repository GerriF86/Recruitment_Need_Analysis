import streamlit as st

def app():
    st.title("Recruitment Summary")
    
    st.subheader("Company Overview")
    st.text_input("Mission:", value=st.session_state.get("mission", ""))
    st.number_input("Number of Employees:", value=st.session_state.get("employees", 1))
    st.text_input("Plans and Challenges:", value=st.session_state.get("plans", ""))
    st.text_input("Competitive Edge:", value=st.session_state.get("competitive_edge", ""))

    st.subheader("Role-Specific Skills")
    st.text_area("Skills:", value=", ".join(st.session_state.get("selected_skills", [])), height=100)

    st.subheader("Job Description")
    st.text_area("Job Description:", value="\n".join(st.session_state.get("job_description", [])), height=200)

    st.subheader("Role Benefits")
    st.text_area("Benefits:", value=", ".join(st.session_state.get("role_benefits", [])), height=100)