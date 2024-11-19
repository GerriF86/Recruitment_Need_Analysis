import streamlit as st
from multiapp import MultiApp
from pages.Recruiting_App import recruiting_app_content
from pages.Impressum import impressum_content
from pages.Our_Mission import our_mission_content
from pages.About_Us import about_us_content
from pages.The_Magic_Behind import the_magic_behind_content  # Add this import

# Instantiate the MultiApp class
app = MultiApp()

# Register the pages
app.add_app("Recruiting App", recruiting_app_content)
app.add_app("Our Mission", our_mission_content)
app.add_app("About Us", about_us_content)
app.add_app("The Magic Behind the Scenes", the_magic_behind_content)  # Register new page
app.add_app("Impressum", impressum_content)

# Main Page Content
def main_page_content():
    st.title("Recruitment Need Analysis App")
    st.markdown(
        """
        **Empowering Better Recruitment Decisions**

        In the ever-competitive job market, the key to successful recruitment lies in understanding the unique needs of each role. Our Recruitment Need Analysis App is designed to help organizations avoid critical information loss during the initial stages of hiring. By gathering and structuring job-specific information through intelligent and dynamic questioning, the app ensures clarity, precision, and alignment across stakeholders.

        ### Why Choose Our Solution?
        - **Tailored Insights:** Dive deeper into the "hidden" aspects of job roles—beyond just job titles and descriptions.
        - **Efficiency Redefined:** Streamline your recruitment process by capturing must-have and nice-to-have requirements with precision.
        - **Reduced Turnover:** Hire right the first time by ensuring alignment of expectations between candidates and employers.

        ### Revolutionizing Recruitment
        With our cutting-edge NLP and state-of-the-art technology stack, the app adapts to the complexity of your organizational needs, ensuring no information is left behind. Invest in your recruitment success today!
        """
    )

# Set the main page to run first
if __name__ == "__main__":
    main_page_content()
    app.run()