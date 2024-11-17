import streamlit as st

def app():
    st.title("Role-Specific Benefits Suggestions")

    role_input = st.text_input("Enter the role you're hiring for:", placeholder="E.g., Backend Developer")

    # Generate role-specific benefits
    if st.button("Generate Role Benefits"):
        if role_input:
            benefits = get_suggestions(f"Suggest benefits for a {role_input}")
            st.session_state['role_benefits'] = benefits
        else:
            st.warning("Please enter a role to generate benefits.")

    # Display generated benefits
    if 'role_benefits' in st.session_state:
        st.subheader("Suggested Benefits:")
        st.write(", ".join(st.session_state['role_benefits']))

    # Finalize the summary
    if st.button("Finish and Review Summary"):
        st.session_state['navigate_to'] = 'Summary'