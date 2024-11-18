# pages/Recruiting_App.py
import streamlit as st
from helpers.utils import generate_job_ad_from_llm, sanitize_input, log_response
from transitions import Machine

# Define states, transitions, and questions for recruitment
states = [
    'role_requirements',
    'company_environment_and_benefits',
    'summary',
    'job_ad_generation'
]

transitions = [
    {'trigger': 'next', 'source': 'role_requirements', 'dest': 'company_environment_and_benefits'},
    {'trigger': 'next', 'source': 'company_environment_and_benefits', 'dest': 'summary'},
    {'trigger': 'next', 'source': 'summary', 'dest': 'job_ad_generation'},
    {'trigger': 'reset', 'source': '*', 'dest': 'role_requirements'}
]

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
        self.machine = Machine(model=self, states=states, transitions=transitions, initial='role_requirements')
        self.answers = {}

    def ask_questions(self):
        current_state = self.state
        questions = define_questions.get(current_state, [])
        
        st.subheader(current_state.replace('_', ' ').title())
        for question in questions:
            raw_answer = st.text_input(question, key=question)
            sanitized_answer = sanitize_input(raw_answer)
            self.answers[question] = sanitized_answer

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

        prompt = f"Create a job ad for a {role} position. Key skills include: {skills}. Benefits are: {benefits}."
        job_ad = generate_job_ad_from_llm(prompt)

        response_dict = {
            "job_title": role,
            "responsibilities": skills,
            "benefits": benefits,
            "generated_ad": job_ad
        }
        log_response(response_dict)

        st.write(job_ad)

        if st.button("Reset Process"):
            self.reset()

# Main content function for the Recruiting App
def recruiting_app_content():
    recruitment_app = RecruitingApp()
    if recruitment_app.state == 'job_ad_generation':
        recruitment_app.generate_job_ad()
    elif recruitment_app.state == 'summary':
        recruitment_app.summarize()
    else:
        recruitment_app.ask_questions()
