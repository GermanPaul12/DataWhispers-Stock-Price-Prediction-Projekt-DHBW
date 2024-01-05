import streamlit as st
import cufflinks as cf
import pandas as pd
import numpy as np


# PageConfig
st.set_page_config(page_title='Homepage',page_icon='🏠')
st.sidebar.success('Select a page above ⬆')

# ---- HEADER SECTION ----
with st.container():
    st.title('Data Whispers AG - Stock Price Prediction')
    st.write('You want to see the code? ➡ Check out the [Github Repository](https://github.com/GermanPaul12/DataWhispers-Stock-Price-Prediction-Projekt-DHBW) 💡')
    st.write("\n")
    st.image("./WI-Modelle_Bilder_Zeichnungen/Preview-Website.png", caption='Preview')
    