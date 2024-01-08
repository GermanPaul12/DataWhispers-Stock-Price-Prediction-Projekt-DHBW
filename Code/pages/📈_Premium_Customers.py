import streamlit as st
import requests


def get_stock_data(interval="1mo", symbol="AMRN", range_="5y", region="US"):
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v3/get-chart"

    querystring = {"interval":interval,"symbol":symbol,"range":range_,"region":region,"includePrePost":"false","useYfid":"true","includeAdjustedClose":"true","events":"capitalGain,div,split"}

    headers = {
        "X-RapidAPI-Key": st.secrets.YAHOO_API_KEY,
        "X-RapidAPI-Host": st.secrets.YAHOO_API_HOST
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()


def get_stock_symbol(querystring="APPLE", region="US"):
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/auto-complete"

    querystring = {"q":querystring,"region":region}

    headers = {
        "X-RapidAPI-Key": st.secrets.YAHOO_API_KEY,
        "X-RapidAPI-Host": st.secrets.YAHOO_API_HOST
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()
    
    
# Log in 
# Initialization
pw = st.text_input("Password", type="password")
log_in_button = st.button("Log in")
if pw == "1234" and log_in_button:
    st.info("You are logged in!")
    st.session_state.logged_in = True
    st.empty()
    st.json(get_stock_data())
elif log_in_button:
    st.warning("Wrong Password!")
# Wenn nicht registirert, dann contact us weiterleitung