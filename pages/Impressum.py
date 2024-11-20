# Load configurations from config.toml
try:
    config = toml.load("config.toml")
except FileNotFoundError:
    st.error("Configuration file 'config.toml' not found. Please ensure it exists in the root directory.")
    st.stop()

# Set page configuration using settings from config.toml
st.set_page_config(
    page_title=config["app"].get("page_title", "Recruitment App"),
    page_icon=config["app"].get("page_icon", "🔍"),
    layout=config["app"].get("layout", "wide")
)

# Inject CSS for the background image
background_image_path = "F:/Capstone/Github Repo/Recruitment_Need_Analysis_Wepapp_DS_Capstone/images/screenshot.png"
st.markdown(
    f"""
    <style>
    body {{
        background-image: url("file://{background_image_path}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    .main {{
        background-color: rgba(255, 255, 255, 0.85); /* White background with transparency for content readability */
        padding: 20px;
        border-radius: 10px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Home Page Content
st.title(config["pages"].get("home_page_title", "Welcome to the Recruitment App"))
st.markdown(f"""
    **{config["pages"].get("home_page_subtitle", "Recruitment Made Simple")}**

    Recruiting the right talent is no longer about guesswork or relying solely on intuition—it’s about precision, data, and understanding.
    Our Recruitment Need Analysis tool empowers you to effortlessly pinpoint the skills, experience, and attributes your next hire should possess.
    With a clean, smart, and secure interface, you'll streamline your hiring process, save time, and find the right fit for your organization.

    From data-driven insights to intelligent recommendations, our tool transforms the recruitment journey from complicated to uncomplicated.
    Click the button below to start your analysis and experience how recruitment can be revolutionized, right from the comfort of your browser.
    No more hassle, just results.
""")

# Navigation Button to Recruiting App
if st.button("Go to Recruitment Need Analysis"):
    st.query_params = {"page": "Recruiting_App"}