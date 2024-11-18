import streamlit as st

# Load your CSS file
def local_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load the CSS
local_css("static/css/style.css")

# Example Page Content
st.title("Recruiting App")
st.write("""
Welcome to the Recruitment Analysis Tool. This is where you can start analyzing recruitment requirements. 
The styling has now been updated using custom CSS.
""")

# Adding a sample button to demonstrate the button styling
if st.button("Click Me!"):
    st.write("Button clicked.")
