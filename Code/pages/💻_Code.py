import streamlit as st

st.title("Our Code 💻")

if st.checkbox("Web-Scraping with Selenium"):
    st.code(open("Code/selenium-scraping.py").read())

if st.checkbox("Requirements"):
    st.code(open("Code/requirements.txt").read())   

if st.checkbox("Streamlit"):
    if st.checkbox("Home"):
        st.code(open("Code/🏠_Home.py").read())    
    if st.checkbox("Code"):
        st.code(open("Code/pages/💻_Code.py").read())
    if st.checkbox("Premium Customers"):
        st.code(open("Code/pages/📈_Premium_Customers.py").read())     
    if st.checkbox("Conception and Diagrams"):
        st.code(open("Code/pages/📋_Conception_and_Diagrams.py").read())     
    if st.checkbox("Contact Us"):
        st.code(open("Code/pages/📝_Contact_Us.py").read())   
    if st.checkbox("Our Products"):
        st.code(open("Code/pages/🚀_Our_Products.py").read())      
         
     