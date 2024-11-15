
import streamlit as st

# Page Configuration
st.set_page_config(page_title="Recruitment Need Analysis", page_icon="📄", layout="wide")

# App Title
st.title("Recruitment Need Analysis Web App")
st.subheader("Streamline Job Description Creation for HR Professionals")

# Introduction
st.markdown("""
    This app assists HR professionals in creating comprehensive job descriptions 
    by guiding them through interactive questions. Answer a series of prompts to 
    generate a formatted job description tailored to your needs.
""")

# Step 1: Role Selection
role = st.selectbox(
    "Select the Position:",
    ["Data Scientist", "Data Analyst", "Software Engineer", "Other"]
)

# Step 2: Dynamic Questions Based on Role
st.header("Position-Specific Details")
if role == "Data Scientist":
    specialization = st.multiselect(
        "Choose Specializations:",
        ["Machine Learning", "Statistics", "Deep Learning", "Data Visualization"]
    )
    tools = st.text_input("List Tools/Technologies Required (comma-separated):")
elif role == "Data Analyst":
    focus_area = st.radio(
        "Primary Focus:",
        ["Data Cleaning", "Reporting", "Business Analysis"]
    )
    software = st.text_input("List Key Software Tools (comma-separated):")
else:
    custom_details = st.text_area("Describe the Role in Detail:")

# Step 3: Work Model and Compensation
st.header("Work Environment and Compensation")
work_model = st.selectbox(
    "Select Work Model:",
    ["Onsite", "Remote", "Hybrid"]
)
salary_range = st.slider("Expected Salary Range (in USD):", 30000, 200000, (50000, 100000))

# Step 4: Generate Job Description
if st.button("Generate Job Description"):
    st.subheader("Generated Job Description:")
    
    # Template Job Description
    job_description = f"""
    **Position**: {role}
    **Work Model**: {work_model}
    **Salary Range**: ${salary_range[0]} - ${salary_range[1]}

    """
    if role == "Data Scientist":
        job_description += f"""
        **Specializations**: {", ".join(specialization)}
        **Tools/Technologies**: {tools}
        """
    elif role == "Data Analyst":
        job_description += f"""
        **Focus Area**: {focus_area}
        **Key Software Tools**: {software}
        """
    else:
        job_description += f"""
        **Role Details**: {custom_details}
        """

    st.markdown(job_description)

    # Download Option
    st.download_button(
        label="Download Job Description",
        data=job_description,
        file_name=f"{role}_Job_Description.txt",
        mime="text/plain"
    )
