import streamlit as st

# Log in 
# Initialization
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if not st.session_state.logged_in:
    pw = st.text_input("Password", type="password")
    log_in_button = st.button("Log in")
if pw == "1234" and log_in_button:
    st.info("You are logged in!")
    st.session_state.logged_in = True
    st.empty()
elif log_in_button:
    st.warning("Wrong Password!")
# Wenn nicht registirert, dann contact us weiterleitung