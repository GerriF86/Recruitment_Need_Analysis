# Step 1: Import Libraries
import os
# Install 'transitions' if not available
try:
    from transitions import Machine
except ImportError:
    os.system('pip install transitions')
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
try:
    import openai
except ImportError:
    os.system('pip install openai')
    import openai

try:
    from dotenv import load_dotenv
except ImportError:
    os.system('pip install python-dotenv')
    from dotenv import load_dotenv

# Step 2: Load Environment Variables and Set Up API Key
try:
    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not set in the .env file.")
    openai.api_key = OPENAI_API_KEY
except Exception as e:
    print(f"Error loading API key: {e}")
    exit(1)

# Step 3: Define the State Machine for Conversation Flow
class RecruitmentBot:
    states = ['initial', 'role_requirements', 'company_environment', 'team', 'candidate', 'compensation_benefits', 'recruitment_process', 'final']

    def __init__(self):
        try:
            # Initialize the state machine with the defined states
            self.machine = Machine(model=self, states=RecruitmentBot.states, initial='initial')
            self.responses = {}  # Dictionary to store responses for summary

            # Adding transitions between different conversation states
            self.machine.add_transition(trigger='start', source='initial', dest='role_requirements', before='ask_role')
            self.machine.add_transition(trigger='gather_role_requirements', source='role_requirements', 
                                        dest='company_environment', before='ask_company_env')
            self.machine.add_transition(trigger='gather_company_env', source='company_environment', 
                                        dest='team', before='ask_team')
            self.machine.add_transition(trigger='gather_team', source='team', 
                                        dest='candidate', before='ask_candidate')
            self.machine.add_transition(trigger='gather_candidate', source='candidate', 
                                        dest='compensation_benefits', before='ask_compensation')
            self.machine.add_transition(trigger='gather_compensation', source='compensation_benefits', 
                                        dest='recruitment_process', before='ask_recruitment_process')
            self.machine.add_transition(trigger='gather_recruitment_process', source='recruitment_process', 
                                        dest='final', before='finish_conversation')
        except Exception as e:
            print(f"Error initializing the RecruitmentBot: {e}")
            exit(1)

    # Step 4: Add New Category Dynamically
    def add_new_category(self, category_name, questions):
        try:
            # Add new state for the category
            new_state = category_name.lower().replace(" ", "_")
            self.states.append(new_state)
            self.machine.add_state(new_state)

            # Add transition to and from the new state
            last_state = self.states[-3]  # The state before 'final'
            self.machine.add_transition(trigger=f'gather_{new_state}', source=last_state, dest=new_state, before=f'ask_{new_state}')
            self.machine.add_transition(trigger=f'gather_{new_state}_complete', source=new_state, dest='final', before='finish_conversation')

            # Dynamically add function to ask questions for new category
            def ask_new_category(self):
                for question in questions:
                    self.responses[question] = input(question + " (Press Enter when answered)")

            # Set the function as an attribute to the instance with the correct name
            setattr(self, f'ask_{new_state}', ask_new_category.__get__(self))
        except Exception as e:
            print(f"Error adding new category '{category_name}': {e}")

    # Step 5: Define Functions for Each State to Ask Specific Questions
    def ask_role(self):
        try:
            question = "What are the main requirements for the role?"
            self.responses[question] = input(question + " (Press Enter when answered)")
            # Example decision tree based questioning
            work_location = input("Is the role office-based, remote, or hybrid? (office/remote/hybrid): ").strip().lower()
            self.responses["Work location"] = work_location
            if work_location == 'remote':
                self.responses["Remote work stipend"] = input("Do you provide a remote work stipend? (Press Enter when answered)")
                self.responses["Communication tools for remote work"] = input("What communication tools do you prefer for remote work? (Press Enter when answered)")
            elif work_location == 'hybrid':
                self.responses["Days in office per week"] = input("How many days per week are expected in the office? (Press Enter when answered)")
            else:
                self.responses["Commute preference"] = input("How do you prefer employees to commute to the office? (Press Enter when answered)")
        except Exception as e:
            print(f"Error in 'ask_role' method: {e}")

    def ask_company_env(self):
        try:
            questions = [
                "Can you briefly explain what your company does?",
                "How big is your organization (number of employees, departments, sister organizations, branches)?",
                "How do you differentiate yourself from other employers/competitors? Why do people work for you?"
            ]
            for question in questions:
                self.responses[question] = input(question + " (Press Enter when answered)")
        except Exception as e:
            print(f"Error in 'ask_company_env' method: {e}")

    def ask_team(self):
        try:
            questions = [
                "What does the team look like? (average age, roles, gender ratio, freelancer vs permanent ratio)",
                "What technologies are used in the team? What are the team responsibilities?",
                "How did this job opening come about?",
                "Can you describe the position? (responsibilities, typical workday, projects)"
            ]
            for question in questions:
                self.responses[question] = input(question + " (Press Enter when answered)")
        except Exception as e:
            print(f"Error in 'ask_team' method: {e}")

    def ask_candidate(self):
        try:
            questions = [
                "What are the must-have technical skills (number of years, minimum requirements - create flexibility)?",
                "What are the desired technical skills?",
                "What personal skills are needed? What kind of person fits into your team?",
                "Language requirements (create flexibility)?",
                "Education - certifications, driving license, commuting distance?",
                "Preferred previous employers or roles?",
                "Can you describe your ideal candidate in five words?",
                "What do you value the most?",
            ]
            for question in questions:
                self.responses[question] = input(question + " (Press Enter when answered)")
        except Exception as e:
            print(f"Error in 'ask_candidate' method: {e}")

    def ask_compensation(self):
        try:
            questions = [
                "What is the primary salary range (minimum/maximum)? 13th-month salary, holiday pay?",
                "Bonus structure?",
                "Number of vacation days, expense reimbursements?",
                "Company car/reimbursement, travel costs, parking?",
                "Laptop/phone, pension plan?",
                "Training budget, other benefits?"
            ]
            for question in questions:
                self.responses[question] = input(question + " (Press Enter when answered)")
        except Exception as e:
            print(f"Error in 'ask_compensation' method: {e}")

    def ask_recruitment_process(self):
        try:
            questions = [
                "What does the interview process look like?",
                "First interview: Who (name/position/role relative to the job opening, focus of the interview, questions)?",
                "Second interview: Who (name/position/role relative to the job opening, focus of the interview, questions)?",
                ]
            for question in questions:
                self.responses[question] = input(question + " (Press Enter when answered)")
        except Exception as e:
            print(f"Error in 'ask_recruitment_process' method: {e}")

    # Step 6: Finish Conversation and Save Responses to a Text File
    def finish_conversation(self):
        try:
            print("Thank you for providing all the required information. The conversation is complete.")
            self.generate_summary_txt()
            self.create_job_ad()  # Generate job ad using ChatGPT API
        except Exception as e:
            print(f"Error in 'finish_conversation' method: {e}")

    # Function to generate a text summary of the conversation
    def generate_summary_txt(self):
        try:
            with open("conversation_summary.txt", "w") as file:
                file.write("Recruitment Conversation Summary\n\n")
                for question, response in self.responses.items():
                    file.write(f"{question}: {response}\n\n")
            print("Summary text file has been generated as 'conversation_summary.txt'.")
        except Exception as e:
            print(f"Error generating text summary: {e}")

    # Step 7: Create Job Advertisement Using OpenAI's ChatGPT API
    def create_job_ad(self):
        try:
            prompt = """
            Create a job advertisement based on the following details:
            """
            for question, response in self.responses.items():
                prompt += f"{question}: {response}\n"

            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=300,
                temperature=0.7
            )
            job_ad = response.choices[0].text.strip()

            # Save the generated job ad to a text file
            with open("job_ad.txt", "w") as file:
                file.write(job_ad)

            print("Job advertisement has been generated and saved as 'job_ad.txt'.")
        except openai.error.OpenAIError as e:
            print(f"OpenAI API error: {e}")
        except Exception as e:
            print(f"An error occurred while generating the job ad: {e}")

# Step 8: Initiate and Run the Conversation Bot
bot = RecruitmentBot()

# Example: Adding a new category dynamically
try:
    bot.add_new_category("Work Culture", [
        "Can you describe the work culture in your organization?",
        "What activities does your team do to improve bonding and morale?",
        "How does your company celebrate achievements or milestones?"
    ])
except Exception as e:
    print(f"Error adding new category 'Work Culture': {e}")

while True:
    try:
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
    except Exception as e:
        print(f"An error occurred during the conversation flow: {e}")
