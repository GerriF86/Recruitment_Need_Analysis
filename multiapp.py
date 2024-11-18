import streamlit as st

class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        """
        Add a new application.
        :param title: The title of the app (string)
        :param func: The app content function (callable)
        """
        self.apps.append({"title": title, "function": func})

    def run(self):
        # Apply modern futuristic styling
        self.apply_custom_style()

        # Create a styled sidebar for app selection
        st.sidebar.title("🚀 Recruitment Hub")
        st.sidebar.markdown("### Choose a section:")
        app = st.sidebar.selectbox(
            "",
            self.apps,
            format_func=lambda app: f"📄 {app['title']}"
        )

        # Footer in the sidebar
        st.sidebar.markdown("---")
        st.sidebar.caption("AI-Powered Recruitment Tool © 2024")

        # Run the selected app
        app["function"]()

    def apply_custom_style(self):
        # Modern, futuristic, minimalist CSS
        custom_css = """
        <style>
        /* Sidebar styles */
        [data-testid="stSidebar"] {
            background-color: #1e1e2f; /* Dark futuristic sidebar */
            color: #ffffff;
            font-family: 'Roboto', sans-serif;
        }
        [data-testid="stSidebar"] h1 {
            color: #ff6b6b; /* Vibrant accent color */
        }

        /* Main content area styles */
        .main {
            background-color: #12121a; /* Dark futuristic main area */
            color: #e0e0e0;
            font-family: 'Roboto', sans-serif;
        }

        /* Scrollbar styles */
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-thumb {
            background: #ff6b6b; /* Highlight scrollbar */
            border-radius: 10px;
        }

        /* Button styles */
        button[kind="primary"] {
            background-color: #ff6b6b;
            color: #ffffff;
            border-radius: 10px;
            font-weight: bold;
        }
        button[kind="primary"]:hover {
            background-color: #ff3b3b;
        }

        /* Table styles */
        .css-1d391kg { /* Streamlit default table styling */
            background-color: #1e1e2f; /* Match sidebar color */
            border-color: #ff6b6b; /* Accent color */
        }
        </style>
        """
        st.markdown(custom_css, unsafe_allow_html=True)
