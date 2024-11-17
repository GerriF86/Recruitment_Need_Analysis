import streamlit as st
from multiapp import MultiApp

# Import each page
from pages.Recruiting_App import recruiting_app
from pages.Our_Mission import app as our_mission_app
from pages.about_us import app as about_us_app
from pages.Impressum import app as impressum_app

# Initialize the app
app = MultiApp()

# Add pages
app.add_app("Recruiting App", recruiting_app)
app.add_app("Our Mission", our_mission_app)
app.add_app("About Us", about_us_app)
app.add_app("Impressum", impressum_app)

# Run the app
app.run()