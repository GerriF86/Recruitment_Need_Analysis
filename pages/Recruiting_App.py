import streamlit as st

def recruiting_app():
    st.title("Recruiting App - Start Here")

    # Input details
    st.header("Company Overview")
    mission = st.text_input("What is your company and its mission?", placeholder="E.g., Leverage AI for decision-making.")
    st.session_state['mission'] = mission

    employees = st.number_input("How many employees are in your organization?", min_value=1, step=1)
    st.session_state['employees'] = employees

    plans = st.text_input("What are your company’s plans and challenges for the next year?", placeholder="E.g., Expand markets.")
    st.session_state['plans'] = plans

    competitive_edge = st.text_input("What sets your company apart from competitors?", placeholder="E.g., Employee growth focus.")
    st.session_state['competitive_edge'] = competitive_edge

    # Navigation to the next section
    if st.button("Next"):
        st.session_state['current_page'] = 'role_skills'
