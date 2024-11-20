import streamlit as st

def custom_css():
    """
    Apply custom CSS for styling the app with a modern and professional look.
    """
    st.markdown(
        """
        <style>
        body {
            background-color: #f8f9fa;  /* Light grey background for professional look */
            font-family: 'Roboto', sans-serif;
        }
        h1, h2, h3 {
            color: #343a40;  /* Dark grey for headings */
        }
        .stImage {
            margin-bottom: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def display_about_us():
    """
    Display the 'About Us' page with founder profiles and images.
    """
    # Page Title and Subtitle
    st.title("About Us")
    st.subheader("Meet the Visionaries Behind the Innovation")
    st.write(
        """
        Our Team merge years of expertise with cutting-edge technology to redefine recruitment.
        Our founders, Olivia Esau and Gerrit Fabisch, are industry leaders with unique perspectives and a shared passion for transforming the hiring process.
        """
    )

    st.markdown(
            """
            ### Olivia Esau
            **Expertise:** Recruitment innovation and HR technology  
            **Focus:** Bridging the gap between traditional HR and AI-driven solutions  
            Olivia brings years of experience and a passion for making recruitment smarter, faster, and more human-centered.
            """
        )

   
    st.markdown(
            """
            ### Gerrit Fabisch
            **Expertise:** Executive search and career planning  
            **Focus:** Data-driven recruitment strategies and market insights  
            Gerrit combines strategic thinking with technical expertise to deliver impactful hiring solutions.
            """
        )

def main():
    """
    Main function to run the Streamlit app.
    """
    custom_css()
    display_about_us()

if __name__ == "__main__":
    main()
