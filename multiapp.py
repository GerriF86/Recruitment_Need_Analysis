# multiapp.py

class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        """ Add a new application to the list of apps. """
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
        import streamlit as st

        # Sidebar for app navigation
        st.sidebar.title("Navigation")
        app = st.sidebar.radio(
            'Go to',
            self.apps,
            format_func=lambda app: app['title'])

        # Run the selected app
        app['function']()
