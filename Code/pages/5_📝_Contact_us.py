import streamlit as st
import yagmail
import re  

def emailValid(email):  
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')  
    if re.fullmatch(regex, email):  
        return 1
    else:  
        return 0

st.set_page_config(page_title='Contact us',page_icon='📧')
st.title("Contact us 📧")

st.write('Du möchtest unseren Code sehen? ➡ Klicke hier [Github Repository](https://github.com/GermanPaul12/DataWhispers-Stock-Price-Prediction-Projekt-DHBW) 💡')

# Forms um uns zu kontaktieren.
with st.form("contact_form", clear_on_submit=True):
    st.write("Please fill out the form below:")
    name = st.text_input("Name")
    email = st.text_input("Email")
    message = st.text_area("Message")

    submit_button = st.form_submit_button("Submit")

    if submit_button and name != "" and email != "" and message != "" and emailValid(email):
        st.write("Thanks for your message!")
        # Here you can add code to handle the form data
        # For example, sending an email or storing it in a database
        yag = yagmail.SMTP(st.secrets.mail, st.secrets.app_pw)
        yag.send(subject="Request from Data Whispers Stocks Streamlit Web-App", 
            contents=f"name: {name}\n\nemail: {email}\n\nmessage: {message}")
    elif submit_button and not emailValid(email):
        st.warning("Please provide a valid mail!")
    elif submit_button:
        st.warning("Please fill out all fields!")        