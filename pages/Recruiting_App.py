# Recruiting_App.py
import streamlit as st
from transitions import Machine
import os
import requests

# Define the states for the recruitment process
states = [
    'role_requirements',
    'company_environment_and_benefits',
    'summary',
    'job_ad_generation'
]

# Define the transitions for moving between the states
transitions = [
    {'trigger': 'next', 'source': 'role_requirements', 'dest': 'company_environment_and_benefits'},
    {'trigger': 'next', 'source': 'company_environment_and_benefits', 'dest': 'summary'},
    {'trigger': 'next', 'source': 'summary', 'dest': 'job_ad_generation'},
    {'trigger': 'reset', 'source': '*', 'dest': 'role_requirements'}
]

# Class to manage the recruitment process
define_questions = {
    'role_requirements': [
        "What is the job title for the role?",
        "What are the main responsibilities for this role?",
        "What is the expected start date?"
    ],
    'company_environment_and_benefits': [
        "Describe the team and department environment.",
        "What are the opportunities for growth and training?",
        "What is the salary range for this role?",
        "What benefits does the company provide (e.g., health insurance, retirement plans)?"
    ],
    'summary': [
        "Review the following inputs for the role. Do you want to add anything else?"
    ]
}

class RecruitingApp:
    def __init__(self):
        # Setting up state machine
        self.machine = Machine(model=self, states=states, transitions=transitions, initial='role_requirements')
        self.answers = {}

    def ask_questions(self):
        current_state = self.state
        questions = define_questions.get(current_state, [])
        
        # Streamlit UI for each question
        st.subheader(current_state.replace('_', ' ').title())
        for question in questions:
            self.answers[question] = st.text_input(question, key=question)

        if st.button("Next"):
            self.next()

    def summarize(self):
        st.subheader("Summary of the Role")
        for question, answer in self.answers.items():
            st.write(f"**{question}**: {answer}")

        if st.button("Generate Job Ad"):
            self.next()

        if st.button("Reset Process"):
            self.reset()

    def generate_job_ad(self):
        st.subheader("Generated Job Ad")

        role = self.answers.get("What is the job title for the role?", "")
        skills = self.answers.get("What are the main responsibilities for this role?", "")
        benefits = self.answers.get("What benefits does the company provide (e.g., health insurance, retirement plans)?", "")

        # Prepare prompt for LLM
        prompt = f"Create a job ad for a {role} position. Key skills include: {skills}. Benefits are: {benefits}."

        # Load LLM API URL from environment variable
        API_URL = os.getenv('LLM_API_URL', 'http://localhost:11434/api/generate')

        payload = {
            "prompt": prompt
        }
        headers = {
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(API_URL, json=payload, headers=headers)
            response.raise_for_status()
            llm_output = response.json()
            job_ad = llm_output.get("generated_text", "No text generated.")
        except requests.RequestException as e:
            job_ad = f"An error occurred while generating the job ad: {e}"

        st.write(job_ad)

        if st.button("Reset Process"):
            self.reset()

# Initialize the recruitment app
recruitment_app = RecruitingApp()

# Streamlit logic for rendering the app
if recruitment_app.state == 'job_ad_generation':
    recruitment_app.generate_job_ad()
elif recruitment_app.state == 'summary':
    recruitment_app.summarize()
else:
    recruitment_app.ask_questions()
