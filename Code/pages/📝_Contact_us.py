import streamlit as st
import yagmail
from keyring import get_keyring
get_keyring()

# Forms um uns zu kontaktieren.
with st.form("contact_form", clear_on_submit=True):
    st.write("Please fill out the form below:")
    name = st.text_input("Name")
    email = st.text_input("Email")
    message = st.text_area("Message")

    submit_button = st.form_submit_button("Submit")

    if submit_button:
        st.write("Thanks for your message!")
        # Here you can add code to handle the form data
        # For example, sending an email or storing it in a database
        yag = yagmail.SMTP('automatedbygerman@gmail.com', st.secrets.app_pw)
        