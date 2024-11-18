import streamlit as st
from transitions import Machine
from helpers.utils import generate_job_ad_from_llm, sanitize_input, log_response
import os

# Define states, transitions, and questions
# (This part remains unchanged)

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

        # Use helper function to generate job ad from LLM
        job_ad = generate_job_ad_from_llm(prompt)

        # Log the response for debugging and tracking purposes
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

