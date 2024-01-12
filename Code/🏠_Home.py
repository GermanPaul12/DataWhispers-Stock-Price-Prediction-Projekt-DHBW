import streamlit as st
import cufflinks as cf
import pandas as pd
import numpy as np


# PageConfig
st.set_page_config(page_title='Homepage',page_icon='🏠')
#st.sidebar.success('Select a page above ⬆')

# ---- HEADER SECTION ----
with st.container():
    _, center, _ = st.columns([1,8,1])

    with center:
        st.title("Data Whispers AG")
        st.title(':green[Stock Price Prediction]')
        st.write('You want to see the code? ➡ Check out the [Github Repository](https://github.com/GermanPaul12/DataWhispers-Stock-Price-Prediction-Projekt-DHBW) 💡')
        st.write("""\nWillkommen im Olymp der Finanzwelt, wo die Götter des Reichtums mit goldenen
Aktien jonglieren! "Data Whispers" ist kein gewöhnlicher Name - es ist ein
Versprechen, ein Flüstern der Zukunft, das nur für die Ohren der mutigsten und
kühnsten Investoren bestimmt ist. """)
        st.image("./WI-Modelle_Bilder_Zeichnungen/Preview-Website.png", caption='Preview')
    