
# Step 1: Import Libraries
# Install 'transitions' if not available
try:
    from transitions import Machine
except ImportError:
    import os
    os.system('pip install transitions')
    from transitions import Machine

import json
import random
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Step 2: Define the State Machine for Conversation Flow
class RecruitmentBot:
    states = ['initial', 'role_requirements', 'company_environment', 'team', 'candidate', 'compensation_benefits', 'recruitment_process', 'final']

    def __init__(self):
        # Initialize the state machine with the defined states
        self.machine = Machine(model=self, states=RecruitmentBot.states, initial='initial')

        # Adding transitions between different conversation states
        self.machine.add_transition(trigger='start', source='initial', dest='role_requirements', before='ask_role')
        self.machine.add_transition(trigger='gather_role_requirements', source='role_requirements', dest='company_environment', before='ask_company_env')
        self.machine.add_transition(trigger='gather_company_env', source='company_environment', dest='team', before='ask_team')
        self.machine.add_transition(trigger='gather_team', source='team', dest='candidate', before='ask_candidate')
        self.machine.add_transition(trigger='gather_candidate', source='candidate', dest='compensation_benefits', before='ask_compensation')
        self.machine.add_transition(trigger='gather_compensation', source='compensation_benefits', dest='recruitment_process', before='ask_recruitment_process')
        self.machine.add_transition(trigger='gather_recruitment_process', source='recruitment_process', dest='final', before='finish_conversation')

    # Define functions for each state to ask specific questions
    def ask_role(self):
        input("What are the main requirements for the role? (Press Enter when answered)")
        work_location = input("Is the role office-based, remote, or hybrid? (office/remote/hybrid): ").strip().lower()
        if work_location == 'remote':
            input("Do you provide a remote work stipend? (Press Enter when answered)")
            input("What communication tools do you prefer for remote work? (Press Enter when answered)")
        elif work_location == 'hybrid':
            input("How many days per week are expected in the office? (Press Enter when answered)")
        else:
            input("How do you prefer employees to commute to the office? (Press Enter when answered)")

    def ask_company_env(self):
        questions = [
            "Can you briefly explain what your company does?",
            "How big is your organization (number of employees, departments, sister organizations, branches)?",
            "What are your plans for the near future? What are your biggest challenges?",
            "How do you differentiate yourself from other employers/competitors? Why do people work for you?"
        ]
        for question in questions:
            input(question + " (Press Enter when answered)")

    def ask_team(self):
        questions = [
            "What does the team look like? (average age, roles, gender ratio, freelancer vs permanent ratio)",
            "What technologies are used in the team? What are the team responsibilities?",
            "How did this job opening come about?",
            "Can you describe the position? (responsibilities, typical workday, projects)"
        ]
        for question in questions:
            input(question + " (Press Enter when answered)")

    def ask_candidate(self):
        questions = [
            "What are the must-have technical skills (number of years, minimum requirements - create flexibility)?",
            "What are the desired technical skills?",
            "What personal skills are needed? What kind of person fits into your team?",
            "Language requirements (create flexibility)?",
            "Education - certifications, driving license, commuting distance?",
            "Preferred previous employers or roles?",
            "Can you describe your ideal candidate in five words?",
            "What do you look at first when reviewing a resume?",
            "What do you value the most?",
            "Have you already interviewed candidates and rejected them? Why were they rejected?"
        ]
        for question in questions:
            input(question + " (Press Enter when answered)")

    def ask_compensation(self):
        questions = [
            "What is the primary salary range (minimum/maximum)? 13th-month salary, holiday pay?",
            "Bonus structure?",
            "Number of vacation days, expense reimbursements?",
            "Company car/reimbursement, travel costs, parking?",
            "Laptop/phone, pension plan?",
            "Training budget, other benefits?"
        ]
        for question in questions:
            input(question + " (Press Enter when answered)")

    def ask_recruitment_process(self):
        questions = [
            "Why does this position exist and by when does it need to be filled?",
            "Imagine you cannot fill the position shortly: What impact would this have (on the company/team/manager)? Who is currently taking over the role?",
            "How are resumes evaluated?",
            "When can I expect feedback?",
            "What does the interview process look like?",
            "First interview: Who (name/position/role relative to the job opening, focus of the interview, questions)?",
            "Second interview: Who (name/position/role relative to the job opening, focus of the interview, questions)?",
            "If I had a suitable candidate tomorrow, could you immediately invite them for an interview? When would that be? Create urgency.",
            "Are there already candidates in the process (if so, what phase are they in)?",
            "Have you already engaged other agencies to fill this position? (If so, which ones? Result? Pitch for exclusivity)"
        ]
        for question in questions:
            input(question + " (Press Enter when answered)")

    def finish_conversation(self):
        print("Thank you for providing all the required information. The conversation is complete.")

# Initiate and Run the Conversation Bot
bot = RecruitmentBot()
while True:
    user_input = input("Type 'start' to begin the conversation or 'quit' to exit: ").strip().lower()
    if user_input == 'start':
        bot.start()
        bot.gather_role_requirements()
        bot.gather_company_env()
        bot.gather_team()
        bot.gather_candidate()
        bot.gather_compensation()
        bot.gather_recruitment_process()
    elif user_input == 'quit':
        print("Exiting the conversation.")
        break
    else:
        print("Invalid input. Please type 'start' or 'quit'.")
