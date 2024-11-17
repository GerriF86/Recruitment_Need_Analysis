import streamlit as st
from requests.exceptions import RequestException
from pages.Job_Description import app as job_desc_app


def get_suggestions(prompt):
    """
    Fetch suggestions from the local Llama model using the provided API.
    """
    try:
        response = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={
                "model": "koesn/dolphin-llama3-8b",
                "prompt": prompt,
                "num_ctx": 8192
            },
            stream=True
        )
        response.raise_for_status()
        return response.json().get("text", "").split(",")
    except RequestException as e:
        return [f"Error: Unable to fetch suggestions. Details: {e}"]

def app():
    st.title("Role-Specific Skills Suggestions")

    role_input = st.text_input("Enter the role you're hiring for:", placeholder="E.g., Python Developer")

    # Generate suggestions
    if st.button("Get Skills Suggestions"):
        if role_input:
            skills = get_suggestions(f"Suggest technical skills for a {role_input}")
            st.session_state['skills'] = skills
        else:
            st.warning("Please enter a role to generate skills.")

    # Display suggested skills as clickable buttons
    if "skills" in st.session_state:
        st.subheader("Suggested Skills:")
        cols = st.columns(4)
        for idx, skill in enumerate(st.session_state['skills']):
            with cols[idx % 4]:
                if st.button(skill, key=f"skill_{idx}"):
                    if skill not in st.session_state.get("selected_skills", []):
                        st.session_state.setdefault("selected_skills", []).append(skill)

    # Display selected skills
    if st.session_state.get("selected_skills"):
        st.markdown("### Selected Skills:")
        st.write(", ".join(st.session_state["selected_skills"]))

    # Navigation to the next section
    if st.button("Next"):
        st.session_state['navigate_to'] = 'Job_Description'