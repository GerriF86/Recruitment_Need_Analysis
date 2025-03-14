# app.py

import streamlit as st
from ui_elements import (
    apply_global_styling,
    show_progress_bar,
    show_navigation,
    start_discovery_page,
    company_information_page,
    department_information_page,
    role_description_page,
    task_scope_page,
    skills_competencies_page,
    benefits_compensation_page,
    recruitment_process_page,
    summary_outputs_page
)
from functions import initialize_session_state

def main():
    st.set_page_config(page_title="Vacalyser - An AI-driven job analysis tool", layout="centered")

    # 1. Apply global styling
    apply_global_styling()

    # 2. Initialize session state
    initialize_session_state()

    # 3. Optionally place a top image or brand header
    st.image("images/lama.png")

    # 4. Title & Intro
    st.markdown(
        """
        <div style="text-align:center; margin-bottom:20px;">
            <h1 style="margin-top:0;">Vacalyser</h1>
            <p style="font-size:1.05em;">
               Enhancing hiring workflows with intelligent suggestions and optimizations.<br/>
               By leveraging FAISS for similarity search and LLaMA for generative AI recommendations,<br/>
               it helps users fine-tune job postings and CVs efficiently, ensuring better hiring outcomes. 🚀
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Expanders or additional info
    with st.expander("Who is this Tool for?"):
        st.markdown(
            """
            **Short Description**  
            The Need-Analysis Tool is an AI-powered job evaluation tool that leverages FAISS + RAG + LLaMA 
            to optimize job descriptions, resumes, and hiring processes. It allows users to upload CVs or 
            job postings, automatically extracts company details, and suggests tasks, skills, and benefits. 

            ---
            **Who is this App for?**  
            - ✅ **HR professionals & recruiters** → Optimize job postings & hiring strategies.  
            - ✅ **Hiring managers** → Improve job descriptions.  
            - ✅ **Candidates** → Get AI-powered feedback on CVs & job applications.  
            - ✅ **Companies** → Ensure job descriptions are market-competitive and clearly defined.  
            """
        )

    with st.expander("About the Technology"):
        st.markdown(
            """
            **FAISS** for vector-based similarity search, 
            **LLaMA** for advanced text generation in a local environment, 
            **RAG** approach for retrieval-augmented generation, 
            and **Streamlit** for a friendly UI workflow.

            <br/>
            **Main Steps**:
            1. **Company Info** → auto-extract from job ad
            2. **Role** → user details + AI suggestions
            3. **Tasks & Skills** → guided by local RAG approach
            4. **Benefits** → common perks & region-specific additions
            5. **Recruitment** → define the hiring process
            6. **Summary** → final output & AI-based Job Ad or Interview prep
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    # 5. Build multi-section pages
    sections = [
        {"title": "", "function": start_discovery_page},
        {"title": "Company Info", "function": company_information_page},
        {"title": "Department Info", "function": department_information_page},
        {"title": "Role Description", "function": role_description_page},
        {"title": "Task Scope", "function": task_scope_page},
        {"title": "Required Skills", "function": skills_competencies_page},
        {"title": "Benefits & Compensation", "function": benefits_compensation_page},
        {"title": "Recruitment Process", "function": recruitment_process_page},
        {"title": "Summary & Output", "function": summary_outputs_page},
    ]

    if "current_section" not in st.session_state:
        st.session_state["current_section"] = 0

    current_idx = st.session_state["current_section"]
    total_sections = len(sections)

    # Progress bar
    show_progress_bar(current_idx, total_sections)

    # Section Title (if you want a subheader – optional)
    if sections[current_idx]["title"]:
        st.subheader(f"📌 {sections[current_idx]['title']}")

    # Render the page
    sections[current_idx]["function"]()

    # Next / Previous
    show_navigation(current_idx, total_sections)

if __name__ == "__main__":
    main()
