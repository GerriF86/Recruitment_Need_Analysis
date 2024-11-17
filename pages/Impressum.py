import streamlit as st

def load_impressum_page():
    st.title("Impressum")
    st.subheader("Legal Disclosure")
    st.write("""
        Welcome to our Impressum page. Below you will find all the legal information regarding our company as required by law.
        Please feel free to reach out if you have any questions.
    """)
    
    st.markdown("""
    **Company Information**  
    Name: Example Company GmbH  
    Address: Example Street 42, 12345 Example City, Germany  
    Phone: +49 (0) 123 456 7890  
    Email: contact@example.com  
    """)
    
    st.markdown("""
    **Represented by:**  
    John Doe, CEO
    """)
    
    st.markdown("""
    **Registration Information:**  
    Commercial Register: Amtsgericht Example City  
    Registration Number: HRB 12345
    """)

    st.markdown("""
    **VAT ID:**  
    VAT identification number according to §27 a of the VAT law: DE123456789
    """)