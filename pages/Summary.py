import streamlit as st

def app():
    st.title("Recruitment Summary")

    st.subheader("Company Overview")
    with st.expander("Edit Company Overview"):
        st.text_input("Mission:", value=st.session_state.get("mission", ""), key="mission_edit")
        st.number_input("Number of Employees:", value=st.session_state.get("employees", 1), key="employees_edit")
        st.text_input("Plans and Challenges:", value=st.session_state.get("plans", ""), key="plans_edit")
        st.text_input("Competitive Edge:", value=st.session_state.get("competitive_edge", ""), key="competitive_edge_edit")

    st.subheader("Role-Specific Skills")
    with st.expander("Edit Role-Specific Skills"):
        st.text_area("Skills:", value=", ".join(st.session_state.get("selected_skills", [])), height=100, key="skills_edit")

    st.subheader("Job Description")
    with st.expander("Edit Job Description"):
        st.text_area("Job Description:", value="\n".join(st.session_state.get("job_description", [])), height=200, key="job_desc_edit")

    st.subheader("Role Benefits")
    with st.expander("Edit Role Benefits"):
        st.text_area("Benefits:", value=", ".join(st.session_state.get("role_benefits", [])), height=100, key="role_benefits_edit")

    # Update session state with edited values
    if st.button("Save Changes"):
        st.session_state["mission"] = st.session_state["mission_edit"]
        st.session_state["employees"] = st.session_state["employees_edit"]
        st.session_state["plans"] = st.session_state["plans_edit"]
        st.session_state["competitive_edge"] = st.session_state["competitive_edge_edit"]
        st.session_state["selected_skills"] = st.session_state["skills_edit"].split(", ")
        st.session_state["job_description"] = st.session_state["job_desc_edit"].split("\n")
        st.session_state["role_benefits"] = st.session_state["role_benefits_edit"].split(", ")

    # Provide a button for confirming final submission
    if st.button("Finalize Summary"):
        st.success("Recruitment summary has been finalized.")
