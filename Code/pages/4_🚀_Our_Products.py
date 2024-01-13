import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px

# Asset Allocation Model

def format_euro(num):
    return "{:,.2f}".format(num).replace(',', ' ').replace('.', ',').replace(' ', '.') + '€'

def wealth_distribution_prct(time, interest, risk):
    # Risk
    if risk == "1 (no risk)":
        risk = 1
    elif risk == "2 (little risk)":
        risk = 2
    elif risk == "3 (balanced risk)":
        risk = 3
    elif risk == "4 (high risk high reward)":
        risk = 4
    elif risk == "5 (I don't care if i loose everything)":
        risk = 5
    
    if risk == 5 and time > 5 and interest > 10:
        return 70, 10, 5, 5, 0, 10
    elif risk == 5 and time > 5:
        return 80, 10, 0, 10, 0, 0
    elif risk == 5 and time > 3:
        return 0, 70, 10, 10, 10, 0
    elif risk == 5 and time >= 1:    
        return 0, 100, 0, 0, 0, 0
    elif risk >= 4 and time > 10:
        return 70, 10, 0, 20, 0, 0
    elif risk >= 4 and time > 5:
        return 50, 20, 0, 30, 0, 0
    elif risk >= 4 and time > 3:
        return 0, 50, 0, 50, 0, 0
    elif risk >= 4 and time >= 1:
        return 0, 100, 0, 0, 0, 0
    elif risk >= 3 and time > 10:
        return 50, 20, 0, 30, 0, 0
    elif risk >= 3 and time > 5:
        return 30, 30, 0, 50, 0, 0
    elif risk >= 3 and time > 3:
        return 0, 70, 0, 30, 0, 0
    elif risk >= 3 and time >= 1:    
        return 0, 100, 0, 0, 0, 0
    elif risk >= 2 and time > 10:
        return 30, 30, 0, 50, 0, 0
    elif risk >= 2 and time > 5:
        return 20, 40, 0, 40, 0, 0
    elif time >= 1:
        return 0, 100, 0, 0, 0, 0
    else:
        return 0, 0, 0, 0, 100, 0

def wealth_distribution(money, stocks, bonds, commodities, realEstate, cash, options):
    stocks = money * stocks / 100
    bonds = money * bonds / 100
    commodities = money * commodities / 100
    realEstate = money * realEstate / 100
    cash = money * cash / 100
    options = money * options / 100
    return stocks, bonds, commodities, realEstate, cash, options


def get_wealth_after_t_time(time, stocks, bonds, commodities, realEstate, cash, options):
    data = {"year": [0], "stocks": [stocks], "bonds": [bonds], "commodities": [commodities], "realEstate": [realEstate], "cash": [cash], "options": [options], "money": [stocks + bonds + commodities + realEstate + cash + options]}
    for _ in range(time):
        stocks *= 1.1
        bonds *= 1.03
        commodities *= 1.03
        realEstate *= 1.03
        cash *= 1.02
        options *= 1.15
        data["year"].append(len(data["year"]))
        data["stocks"].append(stocks)
        data["bonds"].append(bonds)
        data["commodities"].append(commodities)
        data["realEstate"].append(realEstate)
        data["cash"].append(cash)
        data["options"].append(options)
        data["money"].append(stocks + bonds + commodities + realEstate + cash + options)
    return data


st.set_page_config(page_title='Our Products',page_icon='📦')
st.title("Our Products 🚀")


with st.expander("Dow Jones Prediction"):
    df = pd.read_csv(r"Code/data/dow_jones_prediction.csv")
    df.set_index("Date", inplace=True)
    fig = px.line(df, x=df.index, y=[column for column in df.columns if column != "Date"], title='Dow Jones Prediction', color_discrete_sequence=px.colors.sequential.RdBu)
    for i in df.columns:
        if i != "Dow Jones" and i != "Date" and i != "all-mpnet-base-v2_umap":
            fig.update_traces(visible='legendonly', selector=dict(name=i))
    st.plotly_chart(fig, use_container_width=True)
    
    df_rmse = pd.read_csv("Code/data/model_rmse_scores.csv")
    
    fig = px.bar(df_rmse, x="Model Name", y="R-squared", title="R-Sqaured Values for Models",color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_xaxes(tickangle=90)
    fig.update_layout(
    # set tick mode to array, tickvals to your vals calculated and tick text  to the text genrated
        yaxis={"tickmode":"array","tickvals":[0.0, 0.2, 0.4, 0.6, 0.8, 1.0], "ticktext":["0.0", "0.2", "0.4", "0.6","0.8", "1.0"]}
        )
    st.plotly_chart(fig, use_container_width=True)
    
    fig = px.bar(df_rmse, x="Model Name", y="RMSE", title="RMSE Values for Models", color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_xaxes(tickangle=90)
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Best model 👑")
    # name
    st.write("BERTOPIC (all-mpnet-base-v2_umap)")
    # rsme
    st.write(f'RMSE: {df_rmse[df_rmse["Model Name"] == "all-mpnet-base-v2_umap"]["RMSE"]}')
    # accuracy
    st.write(f'Accuracy: {df_rmse[df_rmse["Model Name"] == "all-mpnet-base-v2_umap"]["R-squared"]*100:.2f} %')
    # idea behind the model
    st.write("Unsupervised topic generation by clustering similar document and similarity calculation")
    


# Asset Allocation
with st.expander("Wealth Distribution",True):
    with st.form("Wealth Distrubition Q&A"):
        money = st.number_input("How much money do you want to invest?", min_value=1,value=10000, step=10)
        time = st.slider("For how many years are you willing to invest?", min_value=0, max_value=80, value=20)
        interest = st.slider("How much interest in % do you want to make?", min_value=0, max_value=20, value=5)
        risk = st.select_slider("How much risk are you willing to take?", options=["1 (no risk)", "2 (little risk)", "3 (balanced risk)", "4 (high risk high reward)", "5 (I don't care if i loose everything)"], value="3 (balanced risk)")
        form_submit_btn = st.form_submit_button("Submit")
    if form_submit_btn:
        st.info("ℹ️ Our model assumes that you have at least 2-3 months of salary saved for safety measures and fully are able to invest the money amount you have provided us with.")
        if int(risk[0]) < 3 and int(interest) > 10:
            st.warning("You have to be joking. It's unrealistic to make high interest with low risk.")
        if int(risk[0]) < 4 and int(interest) > 15:
            st.warning("Your imagination might be not realistic, since it's unlikely to make high interest with low risk.")    
        stocks, bonds, commodities, realEstate, cash, options = wealth_distribution(money, *wealth_distribution_prct(time, interest, risk)) 
        col1, col2 = st.columns(2)
        with col1:
            with st.form("Ein schöner Kasten"):
                st.write(f"💸 Your Distribution:")
                st.write(f"Your allocation for {format_euro(money)}")
                st.write(f"Stocks: {format_euro(stocks)}")
                st.write(f"Bonds: {format_euro(bonds)}")
                st.write(f"Commodities: {format_euro(commodities)}")
                st.write(f"Real Estate: {format_euro(realEstate)}")
                st.write(f"Cash: {format_euro(cash)}")
                st.write(f"Options: {format_euro(options)}")
                form_submit_btn = st.form_submit_button("Retry")      
        with col2:
            # Create a DataFrame for the pie chart
            df = pd.DataFrame({
                "Category": ["Stocks", "Bonds", "Commodities", "Real Estate", "Cash", "Options"],
                "Values": [stocks, bonds, commodities, realEstate, cash, options]
            })

            # Now create the pie chart using the DataFrame
            fig = px.pie(df, values='Values', names='Category', title="Your Wealth Distribution",
                        color_discrete_sequence=px.colors.sequential.RdBu, hole=0.5)

           # fig.update_traces(textinfo='label+percent', textposition='inside')
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("Estimated Wealth after given time")
        wealth_df = get_wealth_after_t_time(time, stocks, bonds, commodities, realEstate, cash, options)
        fig_wealth = px.bar(wealth_df, x="year", y=["stocks", "bonds", "commodities", "realEstate", "cash", "options"], title="Wealth Calculation", color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_wealth, use_container_width=True)
        
        