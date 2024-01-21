import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
from datetime import timedelta

st.set_page_config(page_title='Our Products',page_icon='📦', layout="wide")
st.title("Our Products 🚀")

# Dow Jones
Base_col1, Base_col2 = st.columns(2)
with Base_col1:
    with st.expander("Dow Jones",True):
        df = pd.read_csv("Code/data/dow_jones_2019-2024.csv")
        df["Date"] = pd.to_datetime(df["Date"])
        df["Average"] = (df["Close"] + df["Open"])//2

        startDate, endDate = df["Date"].min(), df["Date"].max()
        col1, col2 = st.columns(2)
        with col1:
            date1 = pd.to_datetime(st.date_input("Start Date", startDate, min_value=startDate, max_value=endDate-timedelta(4)))
        with col2:
            date2 = pd.to_datetime(st.date_input("End Date", endDate, min_value=startDate+timedelta(4), max_value=endDate))

        df = df[(df["Date"] >= date1) & (df["Date"] <= date2)].copy()
        x,y,error_high,error_low = df["Date"],df["Average"],df["High"],df["Low"]
        
        fillx = np.concatenate([x, x[::-1]])
        filly = np.concatenate([error_high, error_low[::-1]])
        
        fig = px.line(x=x, y=y, title='Dow Jones',color_discrete_sequence=px.colors.sequential.RdBu)
        fig.update_xaxes(title_text='Datum')
        fig.update_yaxes(title_text='Handelvolumen')
        fig.add_trace(go.Scatter(x=fillx, y=filly, fill='toself', fillcolor='rgba(255,12,24,0.2)', 
                                line=dict(color='rgba(255,0,120,0)'), name="Schwankung", hoverinfo='none'))

        tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])
        tab1.plotly_chart(fig, use_container_width=True)
        tab2.dataframe(df,use_container_width=True)
    
with Base_col2:
    with st.expander("Wertpapiere im DAX 40",True):
        url="https://www.tagesschau.de/wirtschaft/boersenkurse/dax-index-846900/"
        with st.spinner():
            df = pd.read_html(url)[-1].drop(columns="Relation")
        st.dataframe(df)
        st.warning("💡 Die Daten werden von der :blue[Infront Financial Technology GmbH] bereitgestellt. Die Kursdaten werden je nach Börse unterschiedlich, mindestens jedoch 15 Minuten, zeitverzögert angezeigt.")
            