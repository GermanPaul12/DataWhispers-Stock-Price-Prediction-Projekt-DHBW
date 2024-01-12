import streamlit as st
import requests
import pandas as pd
import json
import plotly.express as px
import cufflinks as cf


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
#pw = st.text_input("Password", type="password")
#log_in_button = st.button("Log in")
#if pw == "1234" and log_in_button:
#st.info("You are logged in!")
with st.expander("Get stock symbol"):
    st.session_state.logged_in = True
    st.empty()
    col1,col2 = st.columns(2)
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
           
        
            
    

    

#elif log_in_button:
#    st.warning("Wrong Password!")
# Wenn nicht registirert, dann contact us weiterleitung