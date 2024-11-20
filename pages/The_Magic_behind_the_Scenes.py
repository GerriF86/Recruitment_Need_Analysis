import streamlit as st
import toml

#Load configuration from config.toml

try:
    config = toml.load("config.toml")
except FileNotFoundError:
    st.error("Configuration file 'config.toml' not found. Please ensure it exists in the root directory.")
    st.stop()

# Extract the content for the "Behind the Scenes" page
title = config["pages"].get("behind_scenes_title", "Behind the Scenes")
subtitle = config["pages"].get("behind_scenes_subtitle", "")
content = config["pages"].get("behind_scenes_content", "Content not available.")
