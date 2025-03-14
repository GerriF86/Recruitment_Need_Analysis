#ui_elements.py
import streamlit as st
import json
from functions import (
    store_in_state,
    get_from_session_state,
    process_uploaded_file,
    extract_content_from_url,
    fetch_from_llama
)

# --------------------------------------------------
# GLOBAL STYLING (Per PNG & Branding Guidelines)
# --------------------------------------------------
def apply_global_styling():
    """
    Inject custom CSS/HTML for the new layout as shown in your PNG mocks:
    - Comfortaa (or similar) font
    - Dark background (#353536), highlight (#2e3232), text (#b1b3b3)
    - 'Card'-style containers for each section
    - Styled buttons, progress bar, etc.
    """
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Comfortaa:wght@300;400;700&display=swap');

        body, div, p, button, input, label, textarea, select {
            font-family: 'Comfortaa', sans-serif;
            background-color: #353536 !important;
            color: #b1b3b3 !important;
        }

        /* HEADERS */
        h1, h2, h3, h4 {
            color: #ffffff !important;
        }

        /* PROGRESS BAR */
        .stProgress > div > div {
            background-color: #2e3232 !important;
        }

        /* BUTTONS */
        .stButton > button {
            background-color: #2e3232 !important;
            color: #ffffff !important;
            border: none;
            border-radius: 6px;
            padding: 0.6em 1.2em;
            cursor: pointer;
            font-size: 1rem;
        }
        .stButton > button:hover {
            background-color: #454949 !important;
            transition: all 0.2s ease;
        }

        /* FILE UPLOADER */
        .stFileUploader > label {
            color: #b1b3b3 !important;
        }

        /* 'CARD'-STYLE DIV CONTAINERS */
        .card {
            background-color: #2e3232;
            padding: 1.2rem;
            border-radius: 8px;
            margin-bottom: 1.5rem;
        }

        /* This helps center expansions / text, if needed */
        .expander .streamlit-expanderHeader {
            color: #b1b3b3 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# --------------------------------------------------
# 1) PROGRESS BAR + NAVIGATION
# --------------------------------------------------
def show_progress_bar(current_page, total_pages):
    progress_val = (current_page + 1) / total_pages
    st.progress(progress_val)

def show_navigation(current_page, total_pages):
    """
    Displays Next/Previous buttons, updates st.session_state["current_section"].
    """
    col1, col2, col3 = st.columns([2, 1, 2])

    with col1:
        if current_page > 0:
            if st.button("⬅ Previous"):
                st.session_state["current_section"] -= 1
                st.experimental_rerun()

    with col3:
        if current_page < total_pages - 1:
            if st.button("Next ➡"):
                st.session_state["current_section"] += 1
                st.experimental_rerun()

# --------------------------------------------------
# 2) START DISCOVERY PAGE
# --------------------------------------------------
def start_discovery_page():
    st.header("🔍 Start Discovery: Vacalyzer")

    st.write("Enter a Job Title, optionally a link or an uploaded file. We’ll do our best to auto-fill fields.")

    with st.container():
        colA, colB = st.columns([1, 1])

        with colA:
            job_title = st.text_input("Enter a **Job Title**", get_from_session_state("job_title", ""))
            store_in_state("job_title", job_title)

            input_url = st.text_input("🔗 Enter URL (Job Ad or Company Website)", get_from_session_state("input_url", ""))
            store_in_state("input_url", input_url)

        with colB:
            uploaded_file = st.file_uploader("📂 Upload Job Ad (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])
            if uploaded_file:
                text_data = process_uploaded_file(uploaded_file)
                store_in_state("uploaded_file", text_data)

    if st.button("🔍 Analyze Sources"):
        combined_text = ""

        # Extract from URL
        if input_url:
            url_text = extract_content_from_url(input_url)
            if url_text:
                combined_text += url_text

        # Extract from uploaded file
        file_content = get_from_session_state("uploaded_file", {})
        if file_content and "job_description" in file_content:
            combined_text += "\n" + file_content["job_description"]

        if not combined_text.strip():
            st.warning("No text found to analyze.")
            return

        # AI-driven job ad analysis
        extraction_prompt = f"""
        You are an AI that extracts structured job or company details from the text below.
        Return ONLY valid JSON with these fields:
        - company_name
        - location
        - company_website
        - technologies_used
        - travel_required
        - remote_policy
        - tasks
        - salary_range
        - benefits
        - learning_opportunities
        - health_benefits

        Text to analyze:
        {combined_text}

        Return the JSON object with these keys. If data is not found, use an empty string.
        """

        response_text = fetch_from_llama(extraction_prompt)

        try:
            parsed_json = json.loads(response_text)
            for key in parsed_json:
                store_in_state(key, parsed_json[key])
            st.success("✅ Successfully auto-filled fields from text!")
        except json.JSONDecodeError:
            st.error("❌ Failed to parse JSON from AI response.")

# --------------------------------------------------
# 3) COMPANY INFORMATION PAGE
# --------------------------------------------------
def company_information_page():
    st.header("🏢 Company Information")

    with st.container():
        company_name = st.text_input("Company Name", get_from_session_state("company_name", ""))
        store_in_state("company_name", company_name)

        industry = st.text_input("Industry", get_from_session_state("industry", ""))
        store_in_state("industry", industry)

        location = st.text_input("Location", get_from_session_state("location", ""))
        store_in_state("location", location)

        company_size_opts = ["Small (<50)", "Medium (50-500)", "Large (>500)"]
        c_size_state = get_from_session_state("company_size") or "Small (<50)"
        company_size = st.selectbox("Company Size", company_size_opts, index=company_size_opts.index(c_size_state))
        store_in_state("company_size", company_size)

        founded_val = get_from_session_state("founded_year", 0)
        founded_year = st.number_input("Year Founded", value=int(founded_val), min_value=0, max_value=2100)
        store_in_state("founded_year", founded_year)

        mission = st.text_area("Company Mission & Vision", get_from_session_state("company_mission", ""))
        store_in_state("company_mission", mission)

        website = st.text_input("Company Website / Social Media Links", get_from_session_state("company_website", ""))
        store_in_state("company_website", website)

# --------------------------------------------------
# 4) DEPARTMENT INFORMATION PAGE
# --------------------------------------------------
def department_information_page():
    st.header("🏢 Department Information")

    with st.container():
        department = st.text_input("Department Name", get_from_session_state("department", ""))
        store_in_state("department", department)

        team_size_val = get_from_session_state("team_size") or 0
        team_size = st.number_input("Department Team Size", value=int(team_size_val), min_value=0)
        store_in_state("team_size", team_size)

        direct_supervisor = st.text_input("Direct Supervisor for this Role", get_from_session_state("direct_supervisor", ""))
        store_in_state("direct_supervisor", direct_supervisor)

        department_goals = st.text_area("Departmental Goals", get_from_session_state("department_goals", ""))
        store_in_state("department_goals", department_goals)

        known_techs = ["Python", "JavaScript", "AWS", "Azure", "Salesforce", "SAP"]
        default_techs = get_from_session_state("technologies_used", [])
        selected_techs = st.multiselect("Technologies / Software Used", known_techs, default=default_techs)
        store_in_state("technologies_used", selected_techs)

        travel_required = st.text_area("Travel Requirements", get_from_session_state("travel_required", ""))
        store_in_state("travel_required", travel_required)

        remote_opts = ["None", "Partial", "Fully Remote"]
        default_remote = get_from_session_state("remote_policy", "None")
        remote_policy = st.selectbox("Remote Work Policy", remote_opts, index=remote_opts.index(default_remote))
        store_in_state("remote_policy", remote_policy)

# --------------------------------------------------
# 5) ROLE DESCRIPTION PAGE
# --------------------------------------------------
def role_description_page():
    st.header("👤 Role Description")

    with st.container():
        job_reason_opts = ["New Role", "Growth", "Replacement", "Project-based"]
        default_reason = get_from_session_state("job_reason", "New Role")
        job_reason = st.selectbox("Reason for Hiring", job_reason_opts, index=job_reason_opts.index(default_reason))
        store_in_state("job_reason", job_reason)

        responsibility_distribution = st.text_area(
            "Key Responsibilities (Narrative or %)",
            get_from_session_state("responsibility_distribution", "")
        )
        store_in_state("responsibility_distribution", responsibility_distribution)

        tasks = get_from_session_state("tasks", "")
        tasks_updated = st.text_area("Tasks or main duties for this role", tasks)
        store_in_state("tasks", tasks_updated)

        # If we want to tie tasks more strongly to job title:
        if "job_title" in st.session_state and st.session_state["job_title"]:
            st.write(f"Tasks relevant to **{st.session_state['job_title']}**")

        # Additional info
        job_challenges = st.text_area("Typical Challenges", get_from_session_state("job_challenges", ""))
        store_in_state("job_challenges", job_challenges)

# --------------------------------------------------
# 6) TASK SCOPE PAGE
# --------------------------------------------------
def task_scope_page():
    st.header("🗂️ Task Scope")

    with st.container():
        recurring_tasks = st.text_area("Recurring Tasks (Daily/Weekly/Monthly)", get_from_session_state("recurring_tasks", ""))
        store_in_state("recurring_tasks", recurring_tasks)

        autonomy_level_opts = ["Low", "Medium", "High"]
        default_al = get_from_session_state("autonomy_level", "Low")
        autonomy_level = st.selectbox(
            "Level of Autonomy?",
            autonomy_level_opts,
            index=autonomy_level_opts.index(default_al)
        )
        store_in_state("autonomy_level", autonomy_level)

# --------------------------------------------------
# 7) REQUIRED SKILLS PAGE
# --------------------------------------------------
def skills_competencies_page():
    st.header("🛠️ Required Skills & Competencies")

    with st.container():
        hard_skills = st.text_area("Hard Skills", get_from_session_state("hard_skills", ""))
        store_in_state("hard_skills", hard_skills)

        soft_skills = st.text_area("Soft Skills", get_from_session_state("soft_skills", ""))
        store_in_state("soft_skills", soft_skills)

# --------------------------------------------------
# 8) BENEFITS & COMPENSATION PAGE
# --------------------------------------------------
def benefits_compensation_page():
    st.header("💰 Benefits & Compensation")

    with st.container():
        salary_range = st.text_input("Salary Range", get_from_session_state("salary_range", ""))
        store_in_state("salary_range", salary_range)

        benefits = st.text_area("Key Benefits", get_from_session_state("benefits", ""))
        store_in_state("benefits", benefits)

        health_benefits = st.text_area("Health Benefits", get_from_session_state("health_benefits", ""))
        store_in_state("health_benefits", health_benefits)

        learning_opportunities = st.text_area("Learning & Development Opportunities", get_from_session_state("learning_opportunities", ""))
        store_in_state("learning_opportunities", learning_opportunities)

# --------------------------------------------------
# 9) RECRUITMENT PROCESS PAGE
# --------------------------------------------------
def recruitment_process_page():
    st.header("🏁 Recruitment Process")

    with st.container():
        interview_stages = st.number_input(
            "Number of Interview Rounds",
            value=int(get_from_session_state("interview_stages", 0)),
            min_value=0
        )
        store_in_state("interview_stages", interview_stages)

# --------------------------------------------------
# 10) SUMMARY & OUTPUTS PAGE
# --------------------------------------------------
def summary_outputs_page():
    st.header("📄 Final Summary")

    with st.container():
        st.write("**Job Title**:", get_from_session_state("job_title", "Not provided"))
        st.write("**Company Name**:", get_from_session_state("company_name", ""))
        st.write("**Location**:", get_from_session_state("location", ""))
        st.write("**Website**:", get_from_session_state("company_website", ""))
        st.write("**Responsibilities**:", get_from_session_state("responsibility_distribution", ""))
        st.write("**Salary Range**:", get_from_session_state("salary_range", ""))
        st.write("**Health Benefits**:", get_from_session_state("health_benefits", ""))

        if st.button("🎯 Generate Job Ad"):
            from prompts import generate_job_ad
            job_details = dict(st.session_state)
            job_ad = generate_job_ad(job_details)
            st.subheader("Generated Job Ad")
            st.write(job_ad)

        if st.button("📝 Generate Interview Guide"):
            from prompts import generate_interview_prep
            job_details = dict(st.session_state)
            guide = generate_interview_prep(job_details, "HR")
            st.subheader("Interview Preparation Guide")
            st.write(guide)

    st.info("You can go back and adjust any section, or restart from the beginning.")


