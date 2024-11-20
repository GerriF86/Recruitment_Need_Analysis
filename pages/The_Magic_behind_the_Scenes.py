import streamlit as st

def magic_behind_the_scenes_page():
    st.title("The Magic Behind the Scenes")
    st.markdown("""
    ### The Magic Behind the Scenes
What makes our app so powerful is the combination of state-of-the-art technology and an intelligent design that understands your recruitment needs.

At its core, our app leverages Llama, a large language model, trained on millions of job-related data points and texts. This vast training data allows the model to grasp the nuances of job descriptions, organizational needs, and industry-specific terminology. Imagine having a recruitment expert who has read through millions of job postings and company reports—this is the level of understanding Llama brings to the table.

Key Technical Highlights:
    Harnessing the power of local large language models, intelligent state machines, and graph databases to revolutionize recruitment.
                Millions of Training Data Points:
The Llama model powering our app has been trained on datasets that include:

2 million job descriptions
1.5 million recruitment reviews
Thousands of structured organizational charts
This ensures it understands both the big picture and the small details critical for recruitment success.

                Dynamic Question Flow:
Using a smart state machine model, our app adjusts its questions based on your responses, ensuring no time is wasted on irrelevant details. Each step of the process adapts to the specific needs of your role and organization.

Retrieval-Augmented Generation (RAG):
Our app retrieves the most relevant information from its vast database to ensure accurate and context-specific responses. This makes the system highly reliable and tailored to your needs.
                   
    """)

# Set page configuration
st.set_page_config(page_title="The Magic Behind the Scenes", page_icon="✨", layout="wide")

# Render the Magic Behind the Scenes page
magic_behind_the_scenes_page()
