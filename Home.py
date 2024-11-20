import streamlit as st
import toml
from helpers.utils import custom_css

# Load configurations from config.toml
config = toml.load("config.toml")

# Set page configuration - use settings from config.toml
st.set_page_config(
    page_title=config["app"]["page_title"],
    page_icon=config["app"]["page_icon"],
    layout=config["app"].get("layout", "wide")
)

# Load custom styles
custom_css()

# Main entry point text for home
st.title(config["pages"]["home_page_title"])
st.markdown(f"""
    **{config["pages"]["home_page_subtitle"]}**

Recruiting the right talent is no longer about guesswork or relying solely on intuition—it’s about precision, data, and understanding. Our Recruitment Need Analysis tool empowers you to effortlessly pinpoint the skills, experience, and attributes your next hire should possess. With a clean, smart, and secure interface, you'll streamline your hiring process, save time, and find the right fit for your organization.

From data-driven insights to intelligent recommendations, our tool transforms the recruitment journey from complicated to uncomplicated. Click the button below to start your analysis and experience how recruitment can be revolutionized, right from the comfort of your browser. No more hassle, just results.
""")

# Note: Users will not see this file as an explicit page. The main page will be controlled by the 'pages/' content.
