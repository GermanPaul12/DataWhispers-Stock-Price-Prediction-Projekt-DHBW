import streamlit as st
import yagmail

st.set_page_config(page_title='Contact us',page_icon='📧')
st.title("Contact us 📧")

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
        yag.send(subject="Request from Data Whispers Stocks Streamlit Web-App", 
            contents=f"name: {name}\n\nemail: {email}\n\nmessage: {message}")