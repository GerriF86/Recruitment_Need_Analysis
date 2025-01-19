import streamlit as st
import requests
import json
import re
from PIL import Image

# --- Constants ---
MODEL_NAME = "llama3.2:3b"  # Replace with your preferred model
OLLAMA_URL = "http://localhost:11434/api/generate" or "http://127.0.0.1:11434/api/generate"
# --- Helper Functions ---
def styled_button(label, key=None):
    return st.button(label, key=key)

def parse_bullet_points(text):
    """
    Extracts items from a bullet-point list, handling various bullet styles.
    """
    items = re.findall(r"[-*•]\s*(.*)", text)
    return items

def query_ollama(model_name, input_text):
    """
    Sends a request to the Ollama API, gets a response, and streams it nicely.
    """
    try:
        with requests.post(
            OLLAMA_URL,
            json={"model": model_name, "prompt": input_text},
            stream=True,
        ) as response:
            response.raise_for_status()

            full_response = ""
            for line in response.iter_lines(decode_unicode=True):
                if line.strip():
                    try:
                        json_line = json.loads(line)
                        full_response += json_line.get("response", "")
                    except json.JSONDecodeError:
                        st.error(f"JSON Decode Error: {line}")
                        continue
            return full_response
    except requests.exceptions.RequestException as e:
        st.error(f"Request Error: {e}")
        return ""

# --- Core Functions ---

def analyze_role(job_title):
    """
    Deconstructs a job title into tasks, skills, and challenges.
    """
    if not job_title:
        st.error("Job title: Vanished! Please provide one, I need it.")
        return {
            "tasks": [],
            "technical_skills": [],
            "soft_skills": [],
            "challenges": [],
        }

    prompt = f"""
    Analyze the role of {job_title} in detail:
    * Provide a comprehensive list of common tasks and responsibilities, be very specific.
    * List essential skills and qualifications, both hard and soft skills.
    * Outline potential challenges and opportunities associated with this role.
    """
    response = query_ollama(MODEL_NAME, prompt)

    tasks_section = re.search(r"Common tasks and responsibilities:\n(.*?)(?=Essential skills and qualifications:)", response, re.DOTALL)
    tasks = parse_bullet_points(tasks_section.group(1).strip()) if tasks_section else []
    
    skills_section = re.search(r"Essential skills and qualifications:\n(.*?)(?=Potential challenges and opportunities:)", response, re.DOTALL)
    skills = skills_section.group(1).strip().split("\n\n") if skills_section else []
    technical_skills = parse_bullet_points(skills[0]) if len(skills) > 0 else []
    soft_skills = parse_bullet_points(skills[1]) if len(skills) > 1 else []

    challenges_section = re.search(r"Potential challenges and opportunities:\n(.*)", response, re.DOTALL)
    challenges = parse_bullet_points(challenges_section.group(1).strip()) if challenges_section else []

    return {
        "tasks": tasks,
        "technical_skills": technical_skills,
        "soft_skills": soft_skills,
        "challenges": challenges,
    }

def analyze_company_and_team(job_title):
    """
    Generates 3 insightful questions to probe the company culture and team vibe.
    """
    prompt = f"""
    Develop 3 insightful questions to help a new {job_title} understand the company and team culture, values, and work style.
    """
    response = query_ollama(MODEL_NAME, prompt)
    return {question: "" for question in parse_bullet_points(response)}

def determine_salary(job_title, region, experience):
    """
    Estimates the salary range based on job title, region, and experience.
    """
    prompt = f"""
    Estimate the salary range for a {job_title} with {experience} years of experience in {region}. 
    Provide a realistic salary range and note that this is just an estimate.
    """
    response = query_ollama(MODEL_NAME, prompt)
    match = re.search(r"(\d+)\s*-\s*(\d+)", response)
    return (int(match.group(1)), int(match.group(2))) if match else (None, None)

def generate_job_ad(
    role_info,
    company_info,
    benefits,
    recruitment_process,
    audience="general",
    language="english",
    style="formal",
):
    """
    Creates a job ad.
    """
    prompt = f"""
    Write a {style} job ad in {language} for a {role_info.get('job_title', '')}.

    Target audience: {audience}
    About the company: {company_info}
    Benefits: {benefits}
    Recruitment process: {recruitment_process}

    Include:
    * An engaging company description
    * A clear job description with responsibilities
    * Required skills and qualifications
    * A list of benefits
    * A compelling call to action
    """
    return query_ollama(MODEL_NAME, prompt)

def prepare_interview(role, focus_areas):
    """
    Prepares interview questions that are actually relevant.
    """
    focus_text = ", ".join(focus_areas)
    prompt = f"""
    Generate interview questions for a {role}. Focus on these areas: {focus_text}.
    Provide a mix of behavioral, technical, and situational questions.
    """
    response = query_ollama(MODEL_NAME, prompt)
    return parse_bullet_points(response)

def create_onboarding_checklist(role, department):
    """
    Creates an onboarding checklist that's not just a list of tasks.
    """
    prompt = f"""
    Create a comprehensive onboarding checklist for a {role} in {department}.
    Include tasks, goals, and resources for the first week, first month, and first three months.
    """
    response = query_ollama(MODEL_NAME, prompt)
    return parse_bullet_points(response)

def suggest_retention_strategies(role):
    """
    Suggests ways to keep employees from jumping ship.
    """
    prompt = f"""
    Suggest effective retention strategies for a {role}.
    Consider factors like career growth, work-life balance, recognition, and compensation.
    """
    response = query_ollama(MODEL_NAME, prompt)
    return parse_bullet_points(response)

def identify_benefits(role, region=None):
    """
    Identifies benefits that are actually attractive.
    """
    prompt = f"""
    What are some attractive benefits for a {role}?
    """
    if region:
        prompt += f" Consider the region: {region}."
    response = query_ollama(MODEL_NAME, prompt)
    return parse_bullet_points(response)

def define_recruitment_steps(role):
    """
    Outlines the recruitment process, step-by-step.
    """
    prompt = f"""
    Define the steps in the recruitment process for a {role}.
    Be thorough and include all stages from initial application to offer.
    """
    response = query_ollama(MODEL_NAME, prompt)
    return parse_bullet_points(response)

def get_company_info(company_name):
    """
    Retrieves information about a company.
    """
    prompt = f"""
    Provide information about {company_name}:
    - Industry
    - Company Location
    - Company Size
    - Website
    """
    response = query_ollama(MODEL_NAME, prompt)

    info = {}
    lines = response.split("\n")
    for line in lines:
        if "-" in line:
            key, value = line.split("-", 1)
            key = key.strip()
            value = value.strip()
            if key.lower() == "industry":
                info["Industry"] = value
            elif key.lower() == "company location":
                info["Company Location"] = value
            elif key.lower() == "company size":
                info["Company Size"] = value.lower()
            elif key.lower() == "website":
                info["Website"] = value

    return info

# --- Styling ---
# Function to generate a navigation link
def create_nav_link(page_name, display_text):
    """
    Generates HTML for a styled navigation link.
    """
    st.markdown(
        f"""
        <a href='#' onclick="
            const element = window.parent.document.getElementById('stSessionState');
            element.value = JSON.stringify({{page: '{page_name}'}});
            element.dispatchEvent(new Event('change'));
            return false;
        " class="nav-link">
            {display_text}
        </a>
        """,
        unsafe_allow_html=True
    )

# Inject custom CSS with st.markdown to style the entire app
def load_css():
    st.markdown(
        """
        <style>
        /* General Styling */
        html, body, [class*="st-"] {
            font-family: 'Helvetica Neue', Arial, sans-serif;
        }
        .main {
            background-color: #0e1117;
            color: #e6edf3;
            padding: 1em;
        }
        h1 {
            text-align: center;
            color: #58a6ff;
            font-size: 3em;
            font-weight: 800;
            margin-bottom: 0.5em;
        }
        h2 {
            text-align: center;
            color: #58a6ff;
            font-size: 2em;
            font-weight: 700;
            margin-bottom: 1em;
        }
        h3 {
            color: #58a6ff;
            font-size: 1.5em;
            font-weight: 600;
            margin-bottom: 0.5em;
        }
        .text {
            text-align: center;
            font-size: 1.1em;
            color: #e6edf3;
            margin-bottom: 1.5em;
            line-height: 1.6;
        }

        /* Input & Button Styling */
        .stTextInput input, .stNumberInput input, .stSelectbox select, .stSlider, .stButton>button {
            background-color: #1f2937;
            color: #e6edf3;
            border: 1px solid #58a6ff;
            border-radius: 5px;
            padding: 0.5em;
            margin-bottom: 1em;
        }
        .stButton>button {
            background-color: #58a6ff;
            color: white;
            font-weight: 600;
        }

        /* Checkbox and Radio Button Styling */
        .stCheckbox input, .stRadio input {
            background-color: #1f2937;
            color: #e6edf3;
            border: 1px solid #58a6ff;
        }

        /* Navigation Link Styling */
        .nav-link {
            background-color: #58a6ff;
            color: white;
            padding: 0.5em 1em;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1em;
            font-weight: 600;
            margin: 0 10px;
            text-decoration: none; /* Remove underline from links */
            display: inline-block; /* Ensure links are displayed in a line */
        }
        
        .nav-link:hover {
            background-color: #0e1117;
            color: #58a6ff;
            border: 1px solid #58a6ff;
            text-decoration: none; /* Remove underline on hover */
        }
        
        .nav-link.active {
            background-color: #0e1117;
            color: #58a6ff;
            border: 1px solid #58a6ff;
            text-decoration: none; /* Remove underline on active */
        }

        /* Light Mode Specific Styling */
        .light-mode {
            background-color: #ffffff;
            color: #262730;
        }
        .light-mode .stTextInput input, .light-mode .stNumberInput input, .light-mode .stSelectbox select, .light-mode .stSlider, .light-mode .stButton>button {
            background-color: #f0f2f6;
            color: #262730;
            border: 1px solid #58a6ff;
        }
        .light-mode .stButton>button {
            background-color: #58a6ff;
            color: white;
        }
        .light-mode .nav-link {
            background-color: #58a6ff;
            color: white;
        }
        .light-mode .nav-link:hover {
            background-color: #ffffff;
            color: #58a6ff;
            border: 1px solid #58a6ff;
        }
        .light-mode .nav-link.active {
            background-color: #ffffff;
            color: #58a6ff;
            border: 1px solid #58a6ff;
        }
        .light-mode h1, .light-mode h2, .light-mode h3 {
            color: #0d47a1;
        }
        .light-mode .text {
            color: #262730;
        }
        .light-mode .stCheckbox input, .light-mode .stRadio input {
            background-color: #f0f2f6;
            color: #262730;
            border: 1px solid #58a6ff;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
# --- Helper function to set the theme based on session state ---
def set_theme():
    """
    Sets the app's theme based on the session state.
    """
    if st.session_state.get("light_mode", False):
        st.markdown(
            """
            <script>
                // Function to add the 'light-mode' class to the main div
                function addLightModeClass() {
                    const mainDiv = window.parent.document.querySelector('.main');
                    if (mainDiv) {
                        mainDiv.classList.add('light-mode');
                    }
                }

                // Call the function
                addLightModeClass();
            </script>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <script>
                // Function to remove the 'light-mode' class from the main div
                function removeLightModeClass() {
                    const mainDiv = window.parent.document.querySelector('.main');
                    if (mainDiv) {
                        mainDiv.classList.remove('light-mode');
                    }
                }

                // Call the function
                removeLightModeClass();
            </script>
            """,
            unsafe_allow_html=True
        )

# --- Header Styling ---
def styled_header(title, subtitle):
    """Displays a styled header with title and subtitle."""
    st.markdown(
        f"""
        <div style="text-align: center; margin-bottom: 1em;">
            <h1 style='color: #58a6ff; font-size: 3em; font-weight: 800;'>{title}</h1>
            <h2 style='color: #58a6ff; font-size: 1.8em; font-weight: 700;'>{subtitle}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

# --- Streamlit Navigation ---

def navigate_to_page(page_name):
    """Changes the page."""
    st.session_state.page = page_name

# --- Streamlit Pages ---

def welcome_page():
    """
    The grand entrance. The first impression. Make it count.
    """
    # Use a container for more control over layout
    container = st.container()

    with container:
        st.markdown(
            """
            <style>
            .main {
                background-color: #0d1117; /* Dark background */
                color: #e6edf3; /* Light text */
                padding: 2em;
            }
            .title {
                text-align: center;
                color: #58a6ff; /* Blue for title */
                font-size: 4em;
                font-weight: 800;
                margin-bottom: 0.5em;
            }
            .subtitle {
                text-align: center;
                color: #58a6ff; /* Blue for subtitle */
                font-size: 2.5em;
                font-weight: 600;
                margin-bottom: 1em;
            }
            .text {
                text-align: center;
                font-size: 1.1em; /* Slightly larger text */
                color: #e6edf3; /* Light text */
                margin-bottom: 1.5em;
                line-height: 1.6;
            }
            .input-label {
                font-size: 1.1em;
                color: #58a6ff;
                font-weight: 600;
                margin-bottom: 0.5em;
            }
            .button-text {
                font-size: 1.2em;
                font-weight: 600;
                color: #0d1117; /* Dark text for button */
            }
            .about-section {
                background-color: #1a202c; /* Slightly darker background for About section */
                color: #e6edf3;
                padding: 2em;
                border-radius: 10px;
                margin-top: 2em;
            }
            .about-title {
                color: #58a6ff;
                font-size: 2em;
                font-weight: 700;
                margin-bottom: 1em;
            }
            .about-text {
                font-size: 1em;
                line-height: 1.7;
                margin-bottom: 1em;
            }
            /* Other styles from your original code */
            .st-dd{
                background-color: #58a6ff !important;
            }
            .st-eb {
                background-color: #0e1117 !important;
            }
            .st-f2 {
                color: #58a6ff !important;
            }
            .st-en {
                color: #58a6ff;
            }
            .st-ch, .st-fn {
                background-color: #0e1117 !important;
            }
            .st-bv {
                background-color: transparent;
            }
            .st-de {
                background-color: #0e1117 !important;
            }
            .st-ff, .st-fg {
                background-color: #0e1117;
            }
            .st-c9 {
                color: #58a6ff;
            }
            .st-cb {
                color: #58a6ff;
            }
            .st-ft {
                color: #58a6ff;
            }
            .st-fl {
                color: #58a6ff;
            }
            .st-e5 {
                color: #58a6ff;
            }
            .st-e7 {
                color: #58a6ff;
            }
            .st-fh {
                color: #58a6ff;
            }
            .st-e6 {
                color: #58a6ff;
            }
            .st-fi {
                color: #58a6ff;
            }
            .st-fk {
                color: #58a6ff;
            }
            .st-fc {
                color: #58a6ff;
            }
            .st-d5 {
                background-color: #0e1117;
            }
            .st-b8 {
                background-color: #0e1117;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        # --- HERO SECTION ---
        col1, col2, col3 = st.columns([1, 3, 1])  # Adjust column ratios for a wider central column
        with col2:
            try:
                image = Image.open("data/Home.png")
                st.image(image, width=400)  # Adjust width as needed
            except FileNotFoundError:
                st.error("Image not found. Please make sure 'data/Home.png' exists.")
            except Exception as e:
                st.error(f"An error occurred: {e}")

            st.markdown('<p class="title">RecruitSmarts</p>', unsafe_allow_html=True)
            st.markdown('<p class="subtitle">Revolutionize Your Hiring with AI</p>', unsafe_allow_html=True)

            st.markdown(
                """
                <p class="text">
                Stop losing critical information in the early stages of recruitment.
                <b>RecruitSmarts</b> leverages the power of <b>local AI</b> to help you capture every essential detail about your open positions.
                </p>
                """,
                unsafe_allow_html=True,
            )

            # --- CALL TO ACTION ---
            st.markdown('<p class="input-label">Enter Your Job Title to Begin</p>', unsafe_allow_html=True)
            st.session_state.job_title = st.text_input(
                "",
                value=st.session_state.role_info.get("job_title", ""),
                placeholder="e.g., Data Scientist, Marketing Guru, Python Developer",
                key="job_title_input"
            )

            st.session_state.role_info["job_title"] = st.session_state.job_title

            if st.button("**Start Building Your Ideal Candidate Profile**", key="start_button"):
                navigate_to_page("company_details_page")

def company_details_page():
    # Safely get company name and job title
    company_name = st.session_state.get("company_info", {}).get("Company Name", "the company")
    job_title = st.session_state.role_info["job_title"] # Consistent use of role_info
    styled_header(
        "Tell us about the Company",
        f"Setting the stage for: {job_title} at {company_name}" # Use job_title from role_info
    )

    # --- Section 1: Company Intel ---
    st.subheader("Company Vitals")

    st.session_state.company_info["Company Name"] = st.text_input(
        "Company Name",
        value=st.session_state.company_info["Company Name"],
        placeholder="e.g., Acme Corp"
    )

    if st.session_state.company_info["Company Name"] and styled_button("Autofill Company Intel"):
        with st.spinner("Scouring the web for company info..."):
            retrieved_info = get_company_info(st.session_state.company_info["Company Name"])
            for key, value in retrieved_info.items():
                if key in st.session_state.company_info:
                    st.session_state.company_info[key] = value

    st.session_state.company_info["Company Location"] = st.text_input(
        "Company Location", value=st.session_state.company_info["Company Location"], placeholder="e.g., Silicon Valley, CA"
    )

    employee_ranges = {
        "Startup": ["1-10", "11-50"],
        "Small Biz": ["51-100", "101-250"],
        "Mid-Size": ["251-500", "501-1000"],
        "Enterprise": ["1001-5000", "5000+"],
    }
    selected_range = st.selectbox("**Company Size**", options=list(employee_ranges.keys()))
    st.session_state.company_info["Number of Employees"] = st.selectbox(
        "Employee Count", options=employee_ranges[selected_range], key="employee_range"
    )

    st.session_state.company_info["Department Employees"] = st.slider(
        "Department Size",
        0,
        100,
        value=st.session_state.company_info["Department Employees"],
        key="department_employees",
    )

    top_industries = [
        "Tech",
        "Finance",
        "Healthcare",
        "Retail",
        "Manufacturing",
        "Education",
        "Automotive",
        "Energy",
        "Telecom",
        "Hospitality",
        "Other",
    ]
    try:
        default_industry_index = top_industries.index(st.session_state.company_info["Industry"])
    except ValueError:
        default_industry_index = 0

    st.session_state.company_info["Industry"] = st.selectbox(
        "Industry", options=top_industries, index=default_industry_index
    )

    st.session_state.company_info["Website"] = st.text_input("Website", value=st.session_state.company_info["Website"])

    # --- Section 2: The Hiring Journey ---
    st.subheader("Hiring Process")

    if styled_button("Generate Culture Probes"):
        with st.spinner("Brewing insightful questions..."):
            company_questions = analyze_company_and_team(st.session_state.job_title)
            st.session_state.company_questions = company_questions

    if "company_questions" in st.session_state:
        st.write("**Culture Probe Questions:**")
        if isinstance(st.session_state.company_questions, dict):
            for question in st.session_state.company_questions.keys():
                st.write(f"- {question}")
        else:
            st.error("Hmm, the questions seem to be in a weird format.")

    if styled_button("Map Out Recruitment Steps"):
        with st.spinner("Charting the recruitment journey..."):
            recruitment_steps = define_recruitment_steps(st.session_state.job_title)
            st.session_state.recruitment_process_steps = recruitment_steps

    if "recruitment_process_steps" in st.session_state:
        st.write("**Select the steps in your hiring process:**")
        updated_selected_steps = []
        for step in st.session_state.recruitment_process_steps:
            is_selected = st.checkbox(step)
            if is_selected:
                updated_selected_steps.append(step)
        st.session_state.selected_steps = updated_selected_steps

    if styled_button("Next: Dive into the Role"):
        navigate_to_page("job_details_page")

def job_details_page():
    # Consistent use of role_info for job_title
    job_title = st.session_state.role_info["job_title"]
    styled_header("Role Deep Dive", f"Unpacking the {job_title} Position")

    # Two-column layout
    col1, col2 = st.columns(2)

    with col1:
        st.session_state.role_info["location"] = st.text_input("Location", st.session_state.role_info["location"], placeholder="e.g., Berlin, Germany")
        st.session_state.role_info["work_arrangement"] = st.selectbox(
            "Work Arrangement",
            ["Full-Time", "Part-Time", "Contract", "Internship"],
            index=["Full-Time", "Part-Time", "Contract", "Internship"].index(
                st.session_state.role_info["work_arrangement"]
            ),
        )
        st.session_state.role_info["onsite_remote_hybrid"] = st.selectbox(
            "Onsite / Remote / Hybrid",
            ["Onsite", "Remote", "Hybrid"],
            index=["Onsite", "Remote", "Hybrid"].index(st.session_state.role_info["onsite_remote_hybrid"]),
        )
        if st.session_state.role_info["onsite_remote_hybrid"] == "Hybrid":
            st.session_state.role_info["onsite_percentage"] = st.slider(
                "Onsite Percentage", 0, 100, st.session_state.role_info["onsite_percentage"]
            )

        st.session_state.role_info["department"] = st.text_input("Department", st.session_state.role_info["department"], placeholder="e.g., Engineering")

    with col2:
        min_salary, max_salary = st.session_state.role_info["salary_range"]

        if min_salary is None or min_salary < 0 or min_salary > 200000:
            min_salary = 0

        if max_salary is None or max_salary < 0 or max_salary > 200000:
            max_salary = 0

        salary_range = st.slider(
            "Salary Range (in thousands)",
            0,
            200,
            (min_salary, max_salary),
            10,
            format="%d",
        )
        st.session_state.role_info["salary_range"] = salary_range

        st.session_state.role_info["responsible_money"] = st.text_input(
            "Budget Authority", st.session_state.role_info["responsible_money"], placeholder="e.g., Department Head"
        )
        st.session_state.role_info["responsible_authority"] = st.text_input(
            "Hiring Authority", st.session_state.role_info["responsible_authority"], placeholder="e.g., Hiring Manager"
        )
        st.session_state.role_info["responsible_need"] = st.text_input(
            "Who defines the need?", st.session_state.role_info["responsible_need"], placeholder="e.g., Team Lead"
        )

    if styled_button("Next: Tasks Time"):
        # Call functions using the collected information
        st.session_state.tasks = analyze_role(job_title).get("tasks", []) # Get tasks directly
        st.session_state.selected_tasks = []
        st.session_state.task_frequencies = {} # Initialize task frequencies
        navigate_to_page("tasks_page")

def tasks_page():
    job_title = st.session_state.role_info["job_title"]
    st.header(f"Tasks for {job_title}")

    # Initialize task_frequencies if it doesn't exist
    if "task_frequencies" not in st.session_state:
        st.session_state.task_frequencies = {}

    # Create columns for task selection and frequency
    for task in st.session_state.tasks:
        col1, col2 = st.columns([2, 1])  # Adjust column ratio as needed

        with col1:
            # Checkbox for selecting the task
            if st.checkbox(task, key=f"{task}_checkbox"):
                if task not in st.session_state.selected_tasks:
                    st.session_state.selected_tasks.append(task)
                    
                    # Initialize frequency to "Often" if the task is newly selected
                    if task not in st.session_state.task_frequencies:
                        st.session_state.task_frequencies[task] = "Often"
            else:
                if task in st.session_state.selected_tasks:
                    st.session_state.selected_tasks.remove(task)
                    if task in st.session_state.task_frequencies:
                        del st.session_state.task_frequencies[task]

        with col2:
            # Dropdown for frequency selection, only shown if task is selected
            if task in st.session_state.selected_tasks:
                frequency = st.selectbox(
                    "Frequency",
                    ["Often", "Occasionally", "Rarely"],
                    key=f"{task}_frequency",
                    # Set the current value based on task_frequencies
                    index=["Often", "Occasionally", "Rarely"].index(st.session_state.task_frequencies.get(task, "Often"))
                )
                st.session_state.task_frequencies[task] = frequency

    # Allow adding custom tasks
    manual_task = st.text_input("Add a custom task:", placeholder="e.g., Organize team events")
    if manual_task:
        st.session_state.selected_tasks.append(manual_task)
        st.session_state.task_frequencies[manual_task] = "Often"  # Default to "Often"

    if styled_button("Next: Skillset Selection"):
        navigate_to_page("skills_page")

def skills_page():
    """
    Allows the user to select and prioritize skills, with separate selections for must-have and nice-to-have.
    """
    st.header(f"Skills for {st.session_state.role_info.get('job_title', '')}")
    job_title = st.session_state.role_info.get("job_title", "")

    st.subheader("Technical Skills")
    if styled_button("Generate Technical Skills"):
        if job_title:
            with st.spinner("Generating technical skills..."):
                prompt = f"Generate a list of 15 technologies typically required for the job title '{job_title}', in bullet-point format."
                result = query_ollama(MODEL_NAME, prompt)
                st.session_state.technical_skills = {skill: {"must_have": False, "nice_to_have": False} for skill in parse_bullet_points(result)}
                st.session_state.selected_must_have_technical_skills = []
                st.session_state.selected_nice_to_have_technical_skills = []
        else:
            st.warning("Please enter a job title.")

    # Display technical skills with checkboxes
    if "technical_skills" in st.session_state:
        for skill, skill_data in st.session_state.technical_skills.items():
            col1, col2 = st.columns(2)
            with col1:
                if st.checkbox(f"Must-have: {skill}", value=skill_data["must_have"], key=f"{skill}_must_have_tech"):
                    skill_data["must_have"] = True
                    if skill not in st.session_state.selected_must_have_technical_skills:
                        st.session_state.selected_must_have_technical_skills.append(skill)
                    skill_data["nice_to_have"] = False  # "Must-have" excludes "Nice-to-have"
                else:
                    skill_data["must_have"] = False
                    if skill in st.session_state.selected_must_have_technical_skills:
                        st.session_state.selected_must_have_technical_skills.remove(skill)

            with col2:
                if st.checkbox(f"Nice-to-have: {skill}", value=skill_data["nice_to_have"], key=f"{skill}_nice_to_have_tech"):
                    skill_data["nice_to_have"] = True
                    if skill not in st.session_state.selected_nice_to_have_technical_skills:
                        st.session_state.selected_nice_to_have_technical_skills.append(skill)
                    skill_data["must_have"] = False  # "Nice-to-have" excludes "Must-have"
                else:
                    skill_data["nice_to_have"] = False
                    if skill in st.session_state.selected_nice_to_have_technical_skills:
                        st.session_state.selected_nice_to_have_technical_skills.remove(skill)

        if styled_button("Clear Technical Skills Selections", key="clear_tech"):
            for skill in st.session_state.technical_skills:
                st.session_state.technical_skills[skill]["must_have"] = False
                st.session_state.technical_skills[skill]["nice_to_have"] = False
            st.session_state.selected_must_have_technical_skills = []
            st.session_state.selected_nice_to_have_technical_skills = []

    st.subheader("Soft Skills")
    if styled_button("Generate Soft Skills"):
        if job_title:
            with st.spinner("Generating soft skills..."):
                prompt = f"Generate a list of 15 soft skills typically required for the job title '{job_title}', in bullet-point format."
                result = query_ollama(MODEL_NAME, prompt)
                st.session_state.soft_skills = {skill: {"must_have": False, "nice_to_have": False} for skill in parse_bullet_points(result)}
                st.session_state.selected_must_have_soft_skills = []
                st.session_state.selected_nice_to_have_soft_skills = []
        else:
            st.warning("Please enter a job title.")

    # Display soft skills with checkboxes
    if "soft_skills" in st.session_state:
        for skill, skill_data in st.session_state.soft_skills.items():
            col1, col2 = st.columns(2)
            with col1:
                if st.checkbox(f"Must-have: {skill}", value=skill_data["must_have"], key=f"{skill}_must_have_soft"):
                    skill_data["must_have"] = True
                    if skill not in st.session_state.selected_must_have_soft_skills:
                        st.session_state.selected_must_have_soft_skills.append(skill)
                    skill_data["nice_to_have"] = False  # "Must-have" excludes "Nice-to-have"
                else:
                    skill_data["must_have"] = False
                    if skill in st.session_state.selected_must_have_soft_skills:
                        st.session_state.selected_must_have_soft_skills.remove(skill)

            with col2:
                if st.checkbox(f"Nice-to-have: {skill}", value=skill_data["nice_to_have"], key=f"{skill}_nice_to_have_soft"):
                    skill_data["nice_to_have"] = True
                    if skill not in st.session_state.selected_nice_to_have_soft_skills:
                        st.session_state.selected_nice_to_have_soft_skills.append(skill)
                    skill_data["must_have"] = False  # "Nice-to-have" excludes "Must-have"
                else:
                    skill_data["nice_to_have"] = False
                    if skill in st.session_state.selected_nice_to_have_soft_skills:
                        st.session_state.selected_nice_to_have_soft_skills.remove(skill)

        if styled_button("Clear Soft Skills Selections", key="clear_soft"):
            for skill in st.session_state.soft_skills:
                st.session_state.soft_skills[skill]["must_have"] = False
                st.session_state.soft_skills[skill]["nice_to_have"] = False
            st.session_state.selected_must_have_soft_skills = []
            st.session_state.selected_nice_to_have_soft_skills = []

    # Display selected skills
    st.write("Selected Must-have Technical Skills:", ", ".join(st.session_state.get("selected_must_have_technical_skills", [])))
    st.write("Selected Nice-to-have Technical Skills:", ", ".join(st.session_state.get("selected_nice_to_have_technical_skills", [])))
    st.write("Selected Must-have Soft Skills:", ", ".join(st.session_state.get("selected_must_have_soft_skills", [])))
    st.write("Selected Nice-to-have Soft Skills:", ", ".join(st.session_state.get("selected_nice_to_have_soft_skills", [])))

    if styled_button("Next: Benefits Breakdown"):
        # Generate benefits when moving to the benefits page
        with st.spinner("Identifying attractive benefits..."):
            classic_benefits = ["Health Insurance", "Paid Time Off", "Retirement Plan", "Dental Insurance", "Vision Insurance"]
            innovative_benefits = identify_benefits(st.session_state.role_info.get("job_title", ""))
            st.session_state.benefits = {benefit: {"classic": True, "innovative": False} for benefit in classic_benefits}
            st.session_state.benefits.update({benefit: {"classic": False, "innovative": True} for benefit in innovative_benefits})
            st.session_state.selected_benefits = []
        navigate_to_page("benefits_page")

def benefits_page():
    """
    Allows the user to select and add benefits, with separate selections for classic and innovative benefits.
    """
    job_title = st.session_state.role_info["job_title"]
    st.header(f"Benefits for {job_title}")

    # Initialize selected_benefits in session state if it doesn't exist
    if "selected_benefits" not in st.session_state:
        st.session_state.selected_benefits = []

    # Display benefits with checkboxes organized by type
    st.subheader("Classic Benefits")
    for benefit, benefit_type in st.session_state.benefits.items():
        if benefit_type["classic"]:
            if st.checkbox(benefit, key=benefit):
                if benefit not in st.session_state.selected_benefits:
                    st.session_state.selected_benefits.append(benefit)
            else:
                if benefit in st.session_state.selected_benefits:
                    st.session_state.selected_benefits.remove(benefit)

    st.subheader("Innovative Benefits")
    for benefit, benefit_type in st.session_state.benefits.items():
        if benefit_type["innovative"]:
            if st.checkbox(benefit, key=benefit):
                if benefit not in st.session_state.selected_benefits:
                    st.session_state.selected_benefits.append(benefit)
            else:
                if benefit in st.session_state.selected_benefits:
                    st.session_state.selected_benefits.remove(benefit)

    # Allow adding custom benefits
    manual_benefit = st.text_input("Add a custom benefit:", placeholder="e.g., Pet insurance")
    if manual_benefit:
        st.session_state.benefits[manual_benefit] = {"classic": False, "innovative": False}
        st.session_state.selected_benefits.append(manual_benefit)

    # Display selected benefits
    st.write("Selected Benefits:", ", ".join(st.session_state.selected_benefits))

    if styled_button("Next: Recruitment Roadmap"):
        navigate_to_page("recruitment_process_page")

def recruitment_process_page():
    """
    Allows the user to define the recruitment process.
    """
    job_title = st.session_state.role_info["job_title"]
    st.header(f"Recruitment Process for {job_title}")

    # Check if recruitment_process is initialized, if not, initialize it
    if "recruitment_process" not in st.session_state:
        st.session_state.recruitment_process = []

    for step in st.session_state.recruitment_process:
        if st.checkbox(step, key=step):
            if step not in st.session_state.selected_steps:
                st.session_state.selected_steps.append(step)
        else:
            if step in st.session_state.selected_steps:
                st.session_state.selected_steps.remove(step)

    manual_step = st.text_input("Add a custom step:", placeholder="e.g., Culture fit interview")
    if manual_step:
        st.session_state.selected_steps.append(manual_step)

    if styled_button("Next: Summary & Ad Generation"):
        navigate_to_page("summary_page")

def summary_page():
    st.header("Summary")
    company_name = st.session_state.get("company_info", {}).get("Company Name", "the company")

    st.subheader("Company Information")
    st.write(f"**Company Name:** {st.session_state.company_info.get('Company Name', 'N/A')}")
    st.write(f"**Industry:** {st.session_state.company_info.get('Industry', 'N/A')}")
    st.write(f"**Location:** {st.session_state.company_info.get('Company Location', 'N/A')}")
    st.write(f"**Company Size:** {st.session_state.company_info.get('Company Size', 'N/A')}")
    st.write(f"**Number of Employees:** {st.session_state.company_info.get('Number of Employees', 'N/A')}")
    st.write(
        f"**Number of Employees in the Department:** {st.session_state.company_info.get('Department Employees', 'N/A')}"
    )
    st.write(f"**Website:** {st.session_state.company_info.get('Website', 'N/A')}")

    # Consistent use of role_info for job_title in summary_page
    st.subheader("Job Details")
    st.write(f"**Title:** {st.session_state.role_info.get('job_title', 'N/A')} at {company_name}")
    st.write(f"**Location:** {st.session_state.role_info.get('location', 'N/A')}")
    st.write(
        f"**Work Arrangement:** {st.session_state.role_info.get('work_arrangement', 'N/A')}"
    )
    st.write(
        f"**Work Model:** {st.session_state.role_info.get('onsite_remote_hybrid', 'N/A')}"
    )
    if st.session_state.role_info.get("onsite_remote_hybrid") == "Hybrid":
        st.write(
            f"**Onsite Percentage:** {st.session_state.role_info.get('onsite_percentage', 'N/A')}%"
        )
    st.write(f"**Salary Range:** {st.session_state.role_info.get('salary_range', 'N/A')}")
    st.write(f"**Department:** {st.session_state.role_info.get('department', 'N/A')}")
    st.write(
        f"**Responsible for Money:** {st.session_state.role_info.get('responsible_money', 'N/A')}"
    )
    st.write(
        f"**Responsible for Authority:** {st.session_state.role_info.get('responsible_authority', 'N/A')}"
    )
    st.write(
        f"**Responsible for Need:** {st.session_state.role_info.get('responsible_need', 'N/A')}"
    )

    st.subheader("Tasks")
    if st.session_state.selected_tasks:
        for task in st.session_state.selected_tasks:
            frequency = st.session_state.task_frequencies.get(task, "N/A")
            st.write(f"- {task} (Frequency: {frequency})")
    else:
        st.write("No tasks selected.")

    st.subheader("Skills")
    if st.session_state.selected_must_have_technical_skills or st.session_state.selected_nice_to_have_technical_skills:
        st.write("**Technical Skills:**")
        if st.session_state.selected_must_have_technical_skills:
            st.write("*Must-have:*")
            for skill in st.session_state.selected_must_have_technical_skills:
                st.write(f"  - {skill}")
        if st.session_state.selected_nice_to_have_technical_skills:
            st.write("*Nice-to-have:*")
            for skill in st.session_state.selected_nice_to_have_technical_skills:
                st.write(f"  - {skill}")
    else:
        st.write("No technical skills generated yet.")

    if st.session_state.selected_must_have_soft_skills or st.session_state.selected_nice_to_have_soft_skills:
        st.write("**Soft Skills:**")
        if st.session_state.selected_must_have_soft_skills:
            st.write("*Must-have:*")
            for skill in st.session_state.selected_must_have_soft_skills:
                st.write(f"  - {skill}")
        if st.session_state.selected_nice_to_have_soft_skills:
            st.write("*Nice-to-have:*")
            for skill in st.session_state.selected_nice_to_have_soft_skills:
                st.write(f"  - {skill}")
    else:
        st.write("No soft skills generated yet.")

    st.subheader("Benefits")
    if st.session_state.selected_benefits:
        for benefit in st.session_state.selected_benefits:
            st.write(f"- {benefit}")
    else:
        st.write("No benefits selected.")

    st.subheader("Recruitment Process")
    if st.session_state.selected_steps:
        for step in st.session_state.selected_steps:
            st.write(f"- {step}")
    else:
        st.write("No recruitment steps defined.")

    if styled_button("Generate Job Ad"):
        with st.spinner("Generating job advertisement..."):
            job_ad = generate_job_ad(
                st.session_state.role_info,
                st.session_state.company_info,
                st.session_state.selected_benefits,
                st.session_state.selected_steps,
            )
            st.subheader("Job Advertisement")
            st.text_area(
                "Generated Job Advertisement", job_ad, height=600, label_visibility="collapsed"
            )

# --- Main App Logic ---

# Set the initial page and configure the layout
st.set_page_config(page_title="Find your perfect candidate", layout="wide", initial_sidebar_state="collapsed")

# Initialize session state variables
if "page" not in st.session_state:
    st.session_state.page = "welcome_page"
    st.session_state.company_info = {
        "Company Name": "",
        "Company Location": "",
        "Number of Employees": "",
        "Department Employees": 0,
        "Industry": "",
        "Website": "",
    }
    st.session_state.job_title = ""
    st.session_state.role_info = {
        "job_title": "",
        "location": "",
        "work_arrangement": "Full-Time",
        "onsite_remote_hybrid": "Onsite",
        "onsite_percentage": 100,
        "salary_range": (0, 0),
        "department": "",
        "responsible_money": "",
        "responsible_authority": "",
        "responsible_need": "",
    }
    st.session_state.tasks = []
    st.session_state.selected_tasks = []
    st.session_state.task_frequencies = {}
    st.session_state.technical_skills = {}
    st.session_state.soft_skills = {}
    st.session_state.selected_must_have_technical_skills = []
    st.session_state.selected_nice_to_have_technical_skills = []
    st.session_state.selected_must_have_soft_skills = []
    st.session_state.selected_nice_to_have_soft_skills = []
    st.session_state.benefits = {}
    st.session_state.selected_benefits = []
    st.session_state.recruitment_process = []
    st.session_state.recruitment_process_steps = []
    st.session_state.selected_steps = []
    st.session_state.company_questions = {}

# Navigation bar styling
st.markdown(
    """
    <style>
    .navbar {
        display: flex;
        justify-content: center;
        background-color: #0e1117;
        padding: 1em 0;
        margin-bottom: 2em;
    }
    .nav-link {
        background-color: #58a6ff;
        color: white;
        padding: 0.5em 1em;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-size: 1em;
        font-weight: 600;
        margin: 0 10px;
        text-decoration: none;
        transition: background-color 0.3s ease, color 0.3s ease;
    }
    .nav-link:hover {
        background-color: #0e1117;
        color: #58a6ff;
        border: 1px solid #58a6ff;
    }
    .nav-link.active {
        background-color: #0e1117;
        color: #58a6ff;
        border: 1px solid #58a6ff;
    }
    .light-mode .navbar {
        background-color: #ffffff;
    }
    .light-mode .nav-link {
        background-color: #58a6ff;
        color: white;
    }
    .light-mode .nav-link:hover {
        background-color: #ffffff;
        color: #58a6ff;
        border: 1px solid #58a6ff;
    }
    .light-mode .nav-link.active {
        background-color: #ffffff;
        color: #58a6ff;
        border: 1px solid #58a6ff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Create the navigation bar
st.markdown("<div class='navbar'>", unsafe_allow_html=True)
create_nav_link("welcome_page", "Home")
create_nav_link("company_details_page", "Company Details")
create_nav_link("job_details_page", "Job Details")
create_nav_link("tasks_page", "Tasks")
create_nav_link("skills_page", "Skills")
create_nav_link("benefits_page", "Benefits")
create_nav_link("recruitment_process_page", "Recruitment Process")
create_nav_link("summary_page", "Summary")
st.markdown("</div>", unsafe_allow_html=True)

# Add JavaScript for active link highlighting
st.markdown(
    """
    <script>
        const currentPage = window.parent.document.getElementById('stSessionState').value;
        const navLinks = window.parent.document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            const pageName = link.href.split('page=')[1].split('"')[0];
            if (currentPage.includes(pageName)) {
                link.classList.add('active');
            }
        });
    </script>
    """,
    unsafe_allow_html=True
)

# --- Sidebar for additional information or actions ---
with st.sidebar:
    st.subheader("About the App")
    # Use the AI to generate a description of the app
    if st.button('Generate Description'):
        with st.spinner('Generating app description...'):
            description = query_ollama(MODEL_NAME, "Describe an AI-powered talent acquisition app called RecruitSmarts in 3 sentences. Focus on its key features and benefits.")
            st.session_state.app_description = description

    if 'app_description' in st.session_state:
        st.write(st.session_state.app_description)
    else:
        st.write("Click 'Generate Description' to learn about RecruitSmarts.")

# Main navigation logic
if st.session_state.page == "welcome_page":
    welcome_page()
elif st.session_state.page == "company_details_page":
    company_details_page()
elif st.session_state.page == "job_details_page":
    job_details_page()
elif st.session_state.page == "tasks_page":
    tasks_page()
elif st.session_state.page == "skills_page":
    skills_page()
elif st.session_state.page == "benefits_page":
    benefits_page()
elif st.session_state.page == "recruitment_process_page":
    recruitment_process_page()
elif st.session_state.page == "summary_page":
    summary_page()
