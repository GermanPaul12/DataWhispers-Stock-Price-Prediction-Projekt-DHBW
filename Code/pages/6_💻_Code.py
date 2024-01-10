import streamlit as st

st.set_page_config(page_title='Code',page_icon='💻')
st.title("Our Code 💻")

if st.checkbox("Requirements"):
        st.code(open("Code/requirements.txt").read()) 
with st.expander("Here you can check out our trained Models:"):
    if st.checkbox("Article Extractor"):
        st.code(open("Code/models/article_extractor.py").read()) 
    if st.checkbox("Web-Scraping with Selenium"):
        st.code(open("Code/models/selenium-scraping.py").read())
    if st.checkbox("Model based on bertopic"):
        st.code(open("Code/models/bertopic.py").read())
    if st.checkbox("Model based on doc2vec"):
        st.code(open("Code/models/doc2vec.py").read())
    if st.checkbox("Model based on glove2"):
        st.code(open("Code/models/glove2.py").read())

with st.expander("You want to know, how this Website works? Click here to show the used Code"):
    if st.checkbox("🏠 Home"):
        st.code(open("Code/🏠_Home.py").read())    
    if st.checkbox("💻 Code"):
        st.code(open("Code/pages/6_💻_Code.py").read())
    if st.checkbox("📈 Premium Customers"):
        st.code(open("Code/pages/2_📈_Premium_Customers.py").read())     
    if st.checkbox("📋 Conception and Diagrams"):
        st.code(open("Code/pages/3_📋_Conception_and_Diagrams.py").read())     
    if st.checkbox("📝 Contact Us"):
        st.code(open("Code/pages/5_📝_Contact_us.py").read())   
    if st.checkbox("🚀 Our Products"):
        st.code(open("Code/pages/4_🚀_Our_Products.py").read())  
    if st.checkbox("👥 About us"):
        st.code(open("Code/pages/7_👥_About_Us.py").read())          
         
if st.checkbox("Models"):
    # List Python files in the models directory
    model_files = ['article_extractor.py', 'bertopic.py', 'doc2vec.py', 'dov2vec.py', 'glove2.py', 'Key_Feature_Classification.py', 'preprocess.py', 'regression.py', 'preprocess_dow_jones.py', 'selenium-scraping.py', 'sentence_transformer.py']
    
    # Iterate through the list of files and create a checkbox for each one
    for model_file in model_files:
        if st.checkbox(model_file.replace(".py", "")):
            file_path = f"Code/models/{model_file}"  # Path to the model file
            st.code(open(file_path).read())  # Read the contents of the file and display as code
         