import streamlit as st

def our_mission_page():
    st.title("Our Mission")
    st.markdown("""
    ### Empowering Recruitment for the Future
    In the ever-competitive job market, the key to successful recruitment lies in understanding the unique needs of each role. Our Recruitment Need Analysis App is designed to help organizations avoid critical information loss during the initial stages of hiring. By gathering and structuring job-specific information through intelligent and dynamic questioning, the app ensures clarity, precision, and alignment across stakeholders.

Why Choose Our Solution?
Tailored Insights: Dive deeper into the "hidden" aspects of job roles—beyond just job titles and descriptions.
Efficiency Redefined: Streamline your recruitment process by capturing must-have and nice-to-have requirements with precision.
Reduced Turnover: Hire right the first time by ensuring alignment of expectations between candidates and employers..
    """)

# Set page configuration
st.set_page_config(page_title="Our Mission", page_icon="🎯", layout="wide")

# Render the Our Mission page
our_mission_page()
