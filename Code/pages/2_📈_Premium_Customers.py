import streamlit as st
import requests
import pandas as pd
import json
import plotly.express as px
import secrets

st.set_page_config(page_title='Premium Customers', page_icon='💹')
st.title("Premium Customer Dashboard")

# Globale Variablen
LOGIN_KEY = "premium_user_login"     # Schlüssel für den Login-Status
PREMIUM_USERNAME = "testuser"        # Benutzername für Premium-User
PREMIUM_PASSWORD = "test"            # Zufälliges Passwort für Premium-User, perfekt verschlüsselt!

# Login-Funktion


def login_form():
    # Sitzungsvariablen initialisieren
    if not st.session_state.get(LOGIN_KEY):
        st.session_state[LOGIN_KEY] = False
    if st.session_state[LOGIN_KEY]:
        st.write("Du bist angemeldet als Premium-User.\n\n")
        if st.button("Ausloggen"):
            st.session_state[LOGIN_KEY] = False
            st.experimental_rerun()
    else:
        username_input = st.text_input("Benutzername")
        password_input = st.text_input("Passwort", type="password")
        if st.button("Anmelden"):
            if username_input == PREMIUM_USERNAME and password_input == PREMIUM_PASSWORD:
                st.session_state[LOGIN_KEY] = True
                st.success("Du bist jetzt ein Premium-User!")
                st.experimental_rerun()
            else:
                st.error("Invalid Username or Password!\nPlease [📝 Contact us](Contact_us), if you need help!")


login_form()


def get_stock_data(interval="1mo", symbol="AMRN", range_="5y", region="US"):
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v3/get-chart"
    querystring = {"interval": interval, "symbol": symbol, "range": range_, "region": region, "includePrePost": "false", "useYfid": "true", "includeAdjustedClose": "true", "events": "capitalGain,div,split"}
    headers = {
        "X-RapidAPI-Key": st.secrets.YAHOO_API_KEY,
        "X-RapidAPI-Host": st.secrets.YAHOO_API_HOST
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()


def get_stock_symbol(querystring="APPLE", region="US"):
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/auto-complete"
    querystring = {"q": querystring, "region": region}
    headers = {
        "X-RapidAPI-Key": st.secrets.YAHOO_API_KEY,
        "X-RapidAPI-Host": st.secrets.YAHOO_API_HOST
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()


if st.session_state[LOGIN_KEY]:
    with st.expander("📈 Get your Stocks:", True):
        st.session_state.logged_in = True
        st.empty()
        col1, col2 = st.columns(2)
        with col1:
            query_stock_string = st.text_input("Enter a company name")
            query_stock_region = st.selectbox("Select a region", ["US", "BR", "AU", "CA", "FR", "DE", "HK", "IN", "ES", "GB", "SG"])
        with col2:
            st.text('')
            st.text('')
            st.text('')
            st.text('')
            button_to_get_stock_symbol = st.button("Get stock symbol")
            if button_to_get_stock_symbol:
                json_file_stock_symbol = get_stock_symbol(query_stock_string, query_stock_region)
                st.json(json_file_stock_symbol)
                content = json.dumps(json_file_stock_symbol)
                df = pd.read_json(content, orient='index')
                df = df.transpose()
                df.to_csv("Code/data/stock_symbols.csv")
