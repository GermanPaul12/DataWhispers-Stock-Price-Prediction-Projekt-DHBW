import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px

st.set_page_config(page_title='Our Products',page_icon='📦')
st.title("Our Products 🚀")

# Dow Jones
with st.expander("Dow Jones"):
    df = pd.read_csv("Code/data/dow_jones_2019-2024.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    df["Average"] = (df["Close"] + df["Open"])//2

    startDate, endDate = df["Date"].min(), df["Date"].max()
    col1, col2 = st.columns(2)
    with col1:
        date1 = pd.to_datetime(st.date_input("Start Date", startDate))
    with col2:
        date2 = pd.to_datetime(st.date_input("End Date", endDate))

    df = df[(df["Date"] >= date1) & (df["Date"] <= date2)].copy()
    x,y,error_high,error_low = df["Date"],df["Average"],df["High"],df["Low"]

    ## Plotten des Graphen ##
    fig = go.Figure(data=go.Scatter(x=x, y=y, mode='lines', name='Dow Jones'))
    fig.update_layout(title='Dow Jones', xaxis_title='Datum', yaxis_title='Handelvolumen')
    fig.update_shapes(dict(type='rect', xref='x', yref='paper', x0=min(x), y0=0, x1=max(x), y1=1, fillcolor='lightgray', opacity=0.2, line_width=0))
    fillx = np.concatenate([x, x[::-1]])
    filly = np.concatenate([error_high, error_low[::-1]])
    fig.add_trace(go.Scatter(x=fillx, y=filly, fill='toself', fillcolor='rgba(0,176,246,0.2)', line=dict(color='rgba(255,255,255,0)'), name="Tagesschwankung", hoverinfo='none'))

    tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])
    tab1.plotly_chart(fig)
    tab2.write(df.sort_values("Date", ascending=False))
        