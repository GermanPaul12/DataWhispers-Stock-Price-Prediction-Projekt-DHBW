import streamlit as st

st.title("Our Code 💻")

if st.checkbox("Web-Scraping with Selenium"):
    st.code(open("Code/selenium-scraping.py").read())

if st.checkbox("Requirements"):
    st.code(open("Code/requirements.txt").read())   
     