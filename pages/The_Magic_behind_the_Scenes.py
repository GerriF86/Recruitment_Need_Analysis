import streamlit as st

def magic_behind_the_scenes_page():
    st.title("The Magic Behind the Scenes")
    st.markdown("""
    ### Revolutionizing Recruitment with Cutting-Edge Technology

Our app combines state-of-the-art AI, adaptive questioning, and sleek design to streamline the hiring process like never before. By harnessing the power of innovative tools, we ensure that every step, from needs assessment to candidate selection, is efficient, precise, and tailored to your unique requirements.

Key Features:
Llama Model: Trained on 2 million job descriptions and 1.5 million recruitment reviews, it grasps job-specific nuances and organizational needs.
Dynamic Question Flow: Adapts in real-time to your inputs, ensuring role-specific, time-saving questioning.
Retrieval-Augmented Generation (RAG): Delivers context-rich and highly accurate responses by retrieving relevant data.
Neo4j Graph Database: Dynamically handles complex organizational structures for tailored insights.
Streamlined UI/UX: Modern, intuitive interface designed with feedback from 500+ HR experts.
Our mission is to simplify recruitment while maintaining depth and accuracy. With technology built to adapt to your needs, we aim to empower businesses to make smarter, faster, and more impactful hiring decisions.
                   
    """)

# Set page configuration
st.set_page_config(page_title="The Magic Behind the Scenes", page_icon="✨", layout="wide")

# Render the Magic Behind the Scenes page
magic_behind_the_scenes_page()
