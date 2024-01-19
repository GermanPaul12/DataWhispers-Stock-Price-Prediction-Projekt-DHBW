import streamlit as st
import cufflinks as cf
import pandas as pd
import numpy as np


# PageConfig
st.set_page_config(page_title='Homepage',page_icon='🏠', layout="wide")
#st.sidebar.success('Select a page above ⬆')



# ---- HEADER SECTION ----
col1, col2, col3 = st.columns(3)
with col2:
  st.image("Code/img/datawhispers_logo.png", use_column_width=True)
st.markdown('<h1><center>Stock Price Prediction</center><h1>', unsafe_allow_html=True)
st.write("""\nWillkommen im Olymp der Finanzwelt, wo die Götter des Reichtums mit goldenen
Aktien jonglieren! "Data Whispers" ist kein gewöhnlicher Name - es ist ein
Versprechen, ein Flüstern der Zukunft, das nur für die Ohren der mutigsten und
kühnsten Investoren bestimmt ist. """)    

def create_pricing_card(icon, title, price, features, button_text):
  card = """
  <div style="border:1px solid #aaaaaa; border-radius: 10px; padding:2em; margin:1em; height:30em;">
    <div style="display:flex; justify-content:center; font-size: 3em; padding:0.5em;">
      <i class="{}"></i>
    </div>
    <h2 style="text-align:center; margin-bottom:0;">{}</h2>
    <p style="text-align:center; font-size:1.5em; color:#444; margin-top:0.5em;">{}</p>
    <ul style="list-style-type:none; padding:0; margin-top:0.5em;">
      {}
    </ul>
    <div style="display:flex; justify-content:center; margin-top:1em;">
      <a href="Contact_us"><button  style="background-color:#6c5ce7; padding:0.5em 2em; color:white; border-radius:5px;">{}</button></a>
    </div>
  </div>
  """.format(icon, title, price, features, button_text)
  return card

def main():
  st.markdown("""
  <style>
  i {
    font-size: 120px;
    color: #6c5ce7;
  }
  </style>
  <h2>Pricing</h2>
  """, unsafe_allow_html=True)
  
  cols = st.columns(3)
  with cols[0]:
    st.markdown(create_pricing_card("fa fa-star", "Basic", "0€/Monat", "<li style=list-style-type:check>Aktienanalyse</li><li style=list-style-type:check>Dynamische Dax 40</li><li style=list-style-type:check>24/7 Support</li>", "Kostenlos starten"),unsafe_allow_html=True)
  with cols[1]:
    st.markdown(create_pricing_card("fa fa-certificate", "Premium", "25€/Monat", "<li style=list-style-type:check>Individuelle Vermögensberatung</li><li style=list-style-type:check>Premiumuser Dashboard</li><li style=list-style-type:check>Priorisierte Supportanfragen</li>", "Jetzt kaufen"),unsafe_allow_html=True)
  with cols[2]:
    st.markdown(create_pricing_card("fa fa-diamond", "Business", "Let's talk", "<li style=list-style-type:check>Verhandelbare Zusatzleistungen</li><li style=list-style-type:check>Lizenz-Compliance</li><li style=list-style-type:check>Umfassende API</li><li style=list-style-type:check>Reporting</li>", "Kontaktieren"),unsafe_allow_html=True)

main()
