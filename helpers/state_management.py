import streamlit as st
from helpers.llm_utils import generate_role_skills

# State Management Utilities
session_keys = ["page", "company_info", "role_info", "benefits", "recruitment_process", "model_type", "groq_key"]
for key in session_keys:
    st.session_state.setdefault(key, 1 if key == "page" else None)

def change_page(step: int):
    st.session_state.page += step

@st.cache_data
def cached_generate_role_skills(role):
    # Using generate_role_skills from llm_utils.py
    return generate_role_skills(role)

# Caching Skill Generation for Performance
@st.cache_data
def cached_generate_role_skills(role):
    return generate_role_skills(role)
