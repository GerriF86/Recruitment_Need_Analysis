import json
import faiss
import numpy as np
import re
import os
import pandas as pd
from tqdm import tqdm, trange
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import streamlit as st
import requests

# Load environment variables (e.g., API keys for Ollama Llama)
load_dotenv()
ollama_api_key = os.getenv('OLLAMA_API_KEY')

if not ollama_api_key:
    raise ValueError("OLLAMA_API_KEY not found. Please set it in the .env file.")


# Step 2: Load the JSON Files with robust error handling
import os
import pandas as pd
import json

# Step 2: Load the JSON Files with robust error handling
import os
import pandas as pd
import json

# Step 1: Define JSON File Paths
salaries_path = 'data/json/salaries.json'
resumes_path = 'data/json/Entity Recognition in Resumes.json'
it_jobs_path = 'data/json/IT Job Desc Annotated Detailed.json'

# Step 2: Load the JSON Files with robust error handling
try:
    # Ensure the files exist before attempting to read
    for file_path in [salaries_path, resumes_path, it_jobs_path]:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

    # Open each file and check if it contains valid JSON, with explicit utf-8 encoding
    def load_json_file(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                return pd.json_normalize(data)  # Converts JSON object into a DataFrame
            except json.JSONDecodeError as e:
                raise ValueError(f"Error parsing JSON file {file_path}: {e}")

    # Load all datasets
    salaries = load_json_file(salaries_path)
    resumes = load_json_file(resumes_path)
    it_jobs = load_json_file(it_jobs_path)

except (FileNotFoundError, ValueError) as e:
    print(f"Error loading JSON files: {e}")

# # Job Description Generator

# ## Step 1: Initialization
class JobDescriptionGenerator:
    def __init__(self):
        # Initialize data with default values
        self.data = {
            "Position": "N/A",
            "Specialization": "N/A",
            "Work Model": "N/A",
            "Remote Location": "N/A",
            "Remote Timezone": "N/A",
            "Technical Equipment": "N/A",
            "Remote Percentage": "N/A",
            "BI Tools": "N/A",
            "Required Tools": "N/A",
            "Visualization Tools": "N/A",
            "Statistical Methods": "N/A",
            "Big Data Tools": "N/A",
            "Experience Level": "N/A",
            "Leadership Skills": "None",
            "Educational Requirements": "None",
            "Project Leadership": "No",
            "Compensation": "N/A",
            "Home Office Allowance": "None",
            "Remote Benefits": "None",
            "Additional Benefits": "None"
        }
        # Load pre-trained model for embedding generation
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        # Initialize FAISS index for similarity search
        self.index = None
        self.documents = []



    # ## Step 2: Data Cleaning and Preprocessing
    def clean_and_preprocess_dataset(self, dataset):
        # Filter records with missing job descriptions
        filtered_data = dataset[dataset['job_description'].notna()]

        # Extract and normalize job descriptions
        job_descriptions = filtered_data['job_description'].str.strip().str.lower().tolist()

        # Remove duplicates
        unique_job_descriptions = list(set(job_descriptions))

        # Preprocess text to remove special characters
        processed_descriptions = [re.sub(r'[^a-zA-Z0-9\s]', '', desc) for desc in unique_job_descriptions]

        return processed_descriptions

    # ## Step 3: Loading Dataset and Building FAISS Index
    def load_dataset_and_build_index(self, dataset):
        # Clean and preprocess dataset
        print("Cleaning and preprocessing dataset...")
        job_descriptions = self.clean_and_preprocess_dataset(dataset)
        self.documents = job_descriptions

        # Create embeddings for job descriptions with progress report
        print("Generating embeddings...")
        embeddings = []
        for desc in trange(len(job_descriptions), desc="Embedding job descriptions"):
            embedding = self.model.encode(job_descriptions[desc])
            embeddings.append(embedding)
        embeddings = np.array(embeddings)

        # Create a FAISS index and add embeddings
        print("Building FAISS index...")
        if embeddings.size > 0:
            dimension = embeddings.shape[1]
            self.index = faiss.IndexFlatL2(dimension)
            self.index.add(embeddings)
        else:
            print("Error: No embeddings found to build the FAISS index.")

def get_embedding_from_ollama(self, text):
    url = "http://localhost:11434/api/generate"  # Ollama API endpoint
    headers = {
        "Authorization": f"Bearer {ollama_api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-8b-8192",
        "prompt": text
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        # Assuming the Ollama API returns a vector in the 'embedding' field
        embedding = response.json().get('embedding', [])
        return embedding
    except requests.exceptions.RequestException as e:
        print(f"Error getting embedding from Ollama: {e}")
        return []

def get_embedding_from_ollama(self, text):
    url = "http://localhost:11434/api/generate"  # Ollama API endpoint
    headers = {
        "Authorization": f"Bearer {ollama_api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-8b-8192",
        "prompt": text
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        # Assuming the Ollama API returns a vector in the 'embedding' field
        embedding = response.json().get('embedding', [])
        return embedding
    except requests.exceptions.RequestException as e:
        print(f"Error getting embedding from Ollama: {e}")
        return []
def find_similar_jobs(self, query, k=3):
    # Create embedding for the query using Ollama API
    if self.index is None:
        print("Error: FAISS index is not initialized. Please load the dataset and build the index first.")
        return []

    print("Generating embedding for the query...")
    query_embedding = self.get_embedding_from_ollama(query)

    # Search the FAISS index for similar job descriptions
    if query_embedding:
        print("Searching for similar job descriptions...")
        _, indices = self.index.search(np.array([query_embedding]), k)
        # Retrieve and return the top-k most similar job descriptions
        return [self.documents[idx] for idx in indices[0]]
    else:
        print("Error: Could not generate query embedding.")
        return []
def ask_question(self, question, options=None, multiple=False):
    print(question)
    if options:
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        if multiple:
            selected_options = input("Enter the numbers of all applicable options, separated by commas: ")
            return [options[int(choice.strip()) - 1] for choice in selected_options.split(",")]
        else:
            while True:
                try:
                    choice = int(input("Please choose an option: ")) - 1
                    if 0 <= choice < len(options):
                        return options[choice]
                    else:
                        print("Invalid choice. Please enter one of the displayed numbers.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
    else:
        user_input = input("Your question or query: ").strip()
        return user_input
def collect_position_info(self):
    position = self.ask_question("What position are you hiring for?", ["Data Scientist", "Data Analyst"])
    self.data["Position"] = position

    if position == "Data Scientist":
        specialization = self.ask_question("Is there a specific focus for this role?", ["Machine Learning", "Statistics", "Big Data"])
        self.data["Specialization"] = specialization

        if specialization == "Machine Learning":
            ml_focus = self.ask_question("Are there specific machine learning techniques required?", ["Deep Learning", "NLP", "Reinforcement Learning"], multiple=True)
            self.data["Machine Learning Focus"] = ml_focus

            if "Deep Learning" in ml_focus:
                self.data["Frameworks"] = self.ask_question("Are there specific frameworks required?", ["TensorFlow", "Keras", "PyTorch"], multiple=True)
            if "NLP" in ml_focus:
                self.data["NLP Tools"] = self.ask_question("Are there specific NLP libraries or tools that should be used?", ["spaCy", "Hugging Face", "NLTK"], multiple=True)

        elif specialization == "Statistics":
            self.data["Statistical Methods"] = self.ask_text_input("Which statistical methods are particularly important (e.g., regression analysis, ANOVA)?: ")

        elif specialization == "Big Data":
            self.data["Big Data Tools"] = self.ask_text_input("Are there specific Big Data tools the candidate should be proficient with (e.g., Spark, Hadoop)?: ")

        self.data["Tools"] = self.ask_text_input("Please list any specific tools required for this role (e.g., Python, Java, Spark): ")

    # ## Step 6: Collecting Job Information
    def collect_position_info(self):
        position = self.ask_question("What position are you hiring for?", ["Data Scientist", "Data Analyst"])
        self.data["Position"] = position

        if position == "Data Scientist":
            specialization = self.ask_question("Is there a specific focus for this role?", ["Machine Learning", "Statistics", "Big Data"])
            self.data["Specialization"] = specialization

            if specialization == "Machine Learning":
                ml_focus = self.ask_question("Are there specific machine learning techniques required?", ["Deep Learning", "NLP", "Reinforcement Learning"], multiple=True)
                self.data["Machine Learning Focus"] = ml_focus

                if "Deep Learning" in ml_focus:
                    self.data["Frameworks"] = self.ask_question("Are there specific frameworks required?", ["TensorFlow", "Keras", "PyTorch"], multiple=True)
                if "NLP" in ml_focus:
                    self.data["NLP Tools"] = self.ask_question("Are there specific NLP libraries or tools that should be used?", ["spaCy", "Hugging Face", "NLTK"], multiple=True)

            elif specialization == "Statistics":
                self.data["Statistical Methods"] = self.ask_text_input("Which statistical methods are particularly important (e.g., regression analysis, ANOVA)?: ")

            elif specialization == "Big Data":
                self.data["Big Data Tools"] = self.ask_text_input("Are there specific Big Data tools the candidate should be proficient with (e.g., Spark, Hadoop)?: ")

            self.data["Tools"] = self.ask_text_input("Please list any specific tools required for this role (e.g., Python, Java, Spark): ")

        elif position == "Data Analyst":
            focus_area = self.ask_question("What is the main focus for this role?", ["Statistical Analysis", "Business Intelligence", "Data Visualization"])
            self.data["Focus Area"] = focus_area

            if focus_area == "Business Intelligence":
                self.data["BI Tools"] = self.ask_question("Which BI tools should the candidate use?", ["PowerBI", "Tableau", "QlikView"], multiple=True)
                if "PowerBI" in self.data["BI Tools"]:
                    self.data["PowerBI Features"] = self.ask_text_input("Are there specific PowerBI features the candidate should know (e.g., DAX, Power Query)?: ")

            elif focus_area == "Data Visualization":
                self.data["Visualization Tools"] = self.ask_text_input("Which visualization tools are required (e.g., Matplotlib, D3.js, ggplot)?: ")

            self.data["Tools"] = self.ask_text_input("Please list any specific tools required for this role (e.g., Excel, PowerBI, SQL): ")

    def collect_work_model_info(self):
        work_model = self.ask_question("Is the position On-Site, Remote, or Hybrid?", ["On-Site", "Remote", "Hybrid"])
        self.data["Work Model"] = work_model

        if work_model == "Remote":
            self.data["Remote Location"] = self.ask_question("Can the role be remote anywhere in Germany, EU-wide, or globally?", ["Germany", "EU-wide", "Worldwide"])
            self.data["Remote Timezone"] = self.ask_question("Are there timezone or work hour requirements?", ["No specific requirements", "CET timezone preferred", "Fixed working hours required"])
            self.data["Technical Equipment"] = self.ask_question("Will technical equipment be provided for remote work?", ["Yes", "No"])

        elif work_model == "Hybrid":
            self.data["Remote Percentage"] = self.ask_question("What percentage of work is Remote vs. On-Site?", ["70% Remote / 30% On-Site", "50% Remote / 50% On-Site"])

    def collect_qualifications_info(self):
        experience_level = self.ask_question("What level of experience is required for this role?", ["Junior", "Mid-Level", "Senior"])
        self.data["Experience Level"] = experience_level

        if experience_level == "Junior":
            self.data["Educational Requirements"] = self.ask_text_input("Are there specific educational requirements (e.g., Bachelor's in Computer Science)?: ")

        elif experience_level == "Mid-Level":
            self.data["Project Experience"] = self.ask_text_input("What project experience should a mid-level candidate have (e.g., data analysis projects, model training)?: ")

        elif experience_level == "Senior":
            self.data["Project Leadership"] = self.ask_question("Is project leadership experience required?", ["Yes", "No"])
            if self.data["Project Leadership"] == "Yes":
                self.data["Leadership Skills"] = self.ask_text_input("What leadership skills are particularly important (e.g., team leadership, strategic planning)?: ")

    def collect_compensation_info(self):
        self.data["Compensation"] = self.ask_question("What does the compensation package include?", ["Fixed salary", "Variable compensation", "Both"])

        remote_benefits = self.ask_question("Are there specific benefits for remote employees?", ["Yes", "No"])
        if remote_benefits == "Yes":
            # Additional follow-up questions for remote benefits
            benefits = []
            health_benefits = self.ask_text_input("Specify any health benefits (e.g., health insurance, wellness programs): ")
            if health_benefits:
                benefits.append(f"Health Benefits: {health_benefits}")
            
            internet_stipend = self.ask_text_input("Specify if there's an internet stipend or reimbursement: ")
            if internet_stipend:
                benefits.append(f"Internet Stipend: {internet_stipend}")
            
            professional_dev = self.ask_text_input("Specify if there are professional development funds (e.g., training, courses): ")
            if professional_dev:
                benefits.append(f"Professional Development: {professional_dev}")
            
            equipment_allowance = self.ask_text_input("Specify any equipment allowance for remote work: ")
            if equipment_allowance:
                benefits.append(f"Equipment Allowance: {equipment_allowance}")
                
            # Add gathered remote benefits to data
            self.data["Remote Benefits"] = ", ".join(benefits)

            # Allowance follow-up question
            periodicity = self.ask_question("Is the home office allowance provided monthly or yearly?", ["Monthly", "Yearly"])
            amount = self.ask_text_input(f"Enter the {periodicity.lower()} allowance amount (e.g., 50 Euro): ")
            self.data["Home Office Allowance"] = f"{periodicity} {amount}"

    # ## Step 7: Generating Job Description
    def generate_job_description(self):
        description = f"""
        Position: {self.data["Position"]}
        Specialization: {self.data["Specialization"]}
        Work Model: {self.data["Work Model"]}
        Remote Location: {self.data["Remote Location"]}
        Remote Timezone: {self.data["Remote Timezone"]}
        Technical Equipment: {self.data["Technical Equipment"]}
        Remote Percentage: {self.data["Remote Percentage"]}
        BI Tools: {self.data["BI Tools"]}
        Required Tools: {self.data["Tools"]}
        Visualization Tools: {self.data["Visualization Tools"]}
        Statistical Methods: {self.data["Statistical Methods"]}
        Big Data Tools: {self.data["Big Data Tools"]}
        Experience Level: {self.data["Experience Level"]}
        Leadership Skills: {self.data["Leadership Skills"]}
        Educational Requirements: {self.data["Educational Requirements"]}
        Project Leadership: {self.data["Project Leadership"]}
        Compensation: {self.data["Compensation"]}
        Home Office Allowance: {self.data["Home Office Allowance"]}
        Remote Benefits: {self.data["Remote Benefits"]}
        Additional Benefits: {self.data["Additional Benefits"]}
        """
        print("\n--- Generated Job Description ---")
        print(description.strip())

    # ## Step 8: Running the Job Description Generator
    def run(self):
        print("Welcome to the Job Description Generator!")
        self.collect_position_info()
        self.collect_work_model_info()
        self.collect_qualifications_info()
        self.collect_compensation_info()
        self.generate_job_description()


# ## Step 12: Streamlit Application
st.title("Job Description Generator")

# Create an instance of the JobDescriptionGenerator
generator = JobDescriptionGenerator()

# Load dataset and build FAISS index
if st.button("Build Job Description Index"):
    with st.spinner("Building FAISS index..."):
        generator.load_dataset_and_build_index(it_jobs)
