import streamlit as st
import yagmail
import re  

def emailValid(email):  
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')  
    if re.fullmatch(regex, email):  
        return 1
    else:  
        return 0

st.set_page_config(page_title='Contact us',page_icon='📧', layout="wide")
st.title("Contact us 📧")

st.write('You want to see our Code? ➡ Click here: [Github Repository](https://github.com/GermanPaul12/DataWhispers-Stock-Price-Prediction-Projekt-DHBW) 💡')

        
st.write("""
If you have any questions about our services or are considering working with us, 
our team is always at your disposal. Please contact us at:
- Telefon: +49 (123) 456-7890
""")

# Forms um uns zu kontaktieren.
with st.form("contact_form", clear_on_submit=True):
    st.title('E-Mail')
    st.write("Please fill out the form below:")
    name = st.text_input("Name", placeholder='Max Mustermann')
    email = st.text_input("Email", placeholder='Max.Mustermann@mail.com')
    message = st.text_area("Message", placeholder='Your Message')

    submit_button = st.form_submit_button("Submit")

    if submit_button and name != "" and email != "" and message != "" and emailValid(email):
        st.success("Thanks for your message! Your message has been sent, expect a response in the next 3 business days ")
        # Sending the E-Mail via yagmail
        yag = yagmail.SMTP(st.secrets.mail, st.secrets.app_pw)
        yag.send(subject="Request from Data Whispers Stocks Streamlit Web-App", 
            contents=f"name: {name}\n\nemail: {email}\n\nmessage: {message}")
    elif submit_button and not emailValid(email):
        st.warning("Please provide a valid mail!")
    elif submit_button:
        st.warning("Please fill out all fields!")        