import streamlit as st
from multiapp import MultiApp

# Import pages
from pages.Recruiting_App import recruiting_app
from pages.Role_Specific_Skills import app as role_skills_app
from pages.Job_Description import app as job_desc_app
from pages.Role_Benefits import app as role_benefits_app
from pages.Summary import app as summary_app
from pages.Our_Mission import app as our_mission_app
# from pages.about_us import app as about_us_app  # Hidden
# from pages.Impressum import app as impressum_app  # Hidden

# Initialize the MultiApp instance
app = MultiApp()

# Add pages to the app
app.add_app("Home", lambda: st.write("Welcome to the Home Page!"))
app.add_app("Recruiting App", recruiting_app)
app.add_app("Role-Specific Skills", role_skills_app)
app.add_app("Job Description", job_desc_app)
app.add_app("Role Benefits", role_benefits_app)
app.add_app("Summary", summary_app)
app.add_app("Our Mission", our_mission_app)
# app.add_app("About Us", about_us_app)  # Uncomment to show the "About Us" page
# app.add_app("Impressum", impressum_app)  # Uncomment to show the "Impressum" page

# Run the app
app.run()
