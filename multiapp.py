import streamlit as st

class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        """
        Add a new application to the MultiApp.

        Parameters:
        title (str): The title of the app (displayed in the sidebar).
        func (function): The function to render the app.
        """
        self.apps.append({"title": title, "function": func})

    def run(self):
        """
        Run the MultiApp and handle navigation via session state.
        """
        # Ensure session state is initialized for current page
        if 'current_page' not in st.session_state:
            st.session_state['current_page'] = self.apps[0]['title']  # Default to the first app

        # Sidebar navigation
        app_titles = [app['title'] for app in self.apps]

        # Ensure session state is valid
        if st.session_state['current_page'] not in app_titles:
            st.session_state['current_page'] = app_titles[0]  # Default to the first app

        selected_title = st.sidebar.selectbox(
            'Navigation',
            app_titles,
            index=app_titles.index(st.session_state['current_page']),
        )

        # Update session state
        st.session_state['current_page'] = selected_title

        # Run the selected app
        for app in self.apps:
            if app['title'] == selected_title:
                app['function']()
