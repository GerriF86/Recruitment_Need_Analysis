import streamlit as st
import toml
from PIL import Image


# Load configuration from config.toml
try:
    config = toml.load("config.toml")
except FileNotFoundError:
    st.error("Configuration file 'config.toml' not found. Please ensure it exists in the root directory.")
    st.stop()

# Define available pages and their corresponding functions
def home_page():
    st.title(config["pages"].get("home_page_title", "Welcome to the Recruitment App"))
    st.markdown(config["pages"].get("home_page_content", "Content not available."))

def behind_scenes_page():
    st.title(config["pages"].get("behind_scenes_title", "Behind the Scenes"))
    st.markdown(f"### {config['pages'].get('behind_scenes_subtitle', '')}")
    st.markdown(config["pages"].get("behind_scenes_content", "Content not available."))

# Map page names to functions
PAGES = {
    "Home": home_page,
    "Behind the Scenes": behind_scenes_page,
}

# Sidebar Navigation
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))

# Render the selected page
page = PAGES[selection]
page()

# Try loading the image
try:
    image = Image.open(image_path)
    # Display the image
    st.image(image, 
    "https://images.app.goo.gl/du9LJykbi7Dgn6U37",
    caption="Screenshot Example",
    use_column_width=True
    )
except FileNotFoundError:
    st.error(f"Image not found at '{image_path}'. Please check the file path and try again.")
except Exception as e:
    st.error(f"An error occurred while loading the image: {e}")
