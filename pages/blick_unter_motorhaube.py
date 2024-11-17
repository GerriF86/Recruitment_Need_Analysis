import streamlit as st

def blick_unter_die_motorhaube():
    st.title("Blick unter die Motorhaube")
    st.subheader("How the Recruitment Need Analysis Works")
    st.markdown("""
    Here we provide a detailed look under the hood of our Recruitment Need Analysis app. Learn how different AI components work together to create precise job advertisements:

    - **Data Analysis**: We utilize advanced data processing techniques to gather relevant information about your job needs.
    - **Natural Language Processing (NLP)**: Our app uses NLP to understand the nuances of the questions and answers you provide, ensuring high-quality results.
    - **Machine Learning**: The generated job description is powered by state-of-the-art machine learning models, making it unique and tailored to your requirements.

    With our transparent process, you can trust that every aspect of your job advertisement is crafted with expertise.
    """)
    
    st.image("motor.jpg", caption="Behind the Scenes of Recruitment Need Analysis")