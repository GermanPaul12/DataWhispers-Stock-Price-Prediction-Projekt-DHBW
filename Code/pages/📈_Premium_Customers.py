import streamlit as st
import requests

st.set_page_config(page_title='Premium Customers',page_icon='💹')
st.title("Premium Customer Dashboard")
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
    col1,col2,col3,col4 = st.columns(4)
    with col1: query_stock_string = st.text_input("Enter a company name")
    with col2: query_stock_region = st.selectbox("Select a region", ["US", "BR", "AU", "CA", "FR", "DE", "HK", "IN", "ES", "GB", "SG"])
    with col3: button_to_get_stock_symbol = st.button("Get stock symbol", on_click=get_stock_symbol, args=(query_stock_string, query_stock_region))  

elif log_in_button:
    st.warning("Wrong Password!")
# Wenn nicht registirert, dann contact us weiterleitung