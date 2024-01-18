import streamlit as st
import requests
import pandas as pd
import json
import plotly.express as px
import secrets

st.set_page_config(page_title='Premium Customers', page_icon='💹', layout='wide')
st.title("Premium Customer Dashboard")

# Globale Variablen
LOGIN_KEY = "premium_user_login"     # Schlüssel für den Login-Status
PREMIUM_USERNAME = "testuser"        # Benutzername für Premium-User
PREMIUM_PASSWORD = "test"            # Passwort für Premium-User, perfekt verschlüsselt!

# Login-Funktion


def login_form():
    # Sitzungsvariablen initialisieren
    if not st.session_state.get(LOGIN_KEY):
        st.session_state[LOGIN_KEY] = False
    if st.session_state[LOGIN_KEY]:
        col1, col2 = st.columns([5,1])
        with col1:
            st.write("Du bist angemeldet als Premium-User.\n\n")
        with col2:
            if st.button("Ausloggen"):
                st.session_state[LOGIN_KEY] = False
                st.experimental_rerun()
    else:
        with st.form("Anmeldung"):
            username_input = st.text_input("Benutzername")
            password_input = st.text_input("Passwort", type="password")
            if st.form_submit_button("Anmelden"):
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
    
    # Bitcoin API 
    bitcoin_price_url = "https://api.blockchain.com/v3/exchange/tickers/BTC-EUR"

    # Asset Allocation Model

    def format_euro(num):
        return "{:,.2f}".format(num).replace(',', ' ').replace('.', ',').replace(' ', '.') + '€'

    def wealth_distribution_prct(time, interest, risk):
        risk_scale = {"1 (no risk)": 1, 
                    "2 (little risk)": 2, 
                    "3 (balanced risk)": 3, 
                    "4 (high risk high reward)": 4, 
                    "5 (I don't care if i loose everything)": 5}
        risk = risk_scale[risk]
        result = { # (id,Boolean)
            (1 , 5 == risk and 6 <= time and interest > 10): (70, 10, 5, 5, 0, 10),
            (2 , 5 == risk and 6 <= time and True)         : (80, 10, 0, 10, 0, 0),
            (3 , 5 == risk and 4 <= time and True)         : ( 0, 70,10,10,10,  0),
            (4 , 5 == risk and True      and True)         : ( 0,100, 0, 0, 0,  0),
            (5 , 4 <= risk and time > 10 and True)         : (70, 10, 0,20, 0,  0),
            (6 , 4 <= risk and 6 <= time and True)         : (50, 20, 0,30, 0,  0),
            (7 , 4 <= risk and 4 <= time and True)         : ( 0, 50, 0,50, 0,  0),
            (8 , 4 <= risk and True      and True)         : ( 0,100, 0, 0, 0,  0),
            (9 , 3 <= risk and 6 <= time and True)         : (50, 20, 0,30, 0,  0),
            (10, 3 <= risk and 4 <= time and True)         : (30, 30, 0,50, 0,  0),
            (11, 3 <= risk and 3 <= time and True)         : ( 0, 70, 0,30, 0,  0),
            (12, 3 <= risk and True      and True)         : ( 0,100, 0, 0, 0,  0),
            (13, 2 <= risk and 10 < time and True)         : (20, 40, 0,40, 0,  0),
            (14, True      and time >=1  and True)         : ( 0,100, 0, 0, 0,  0),
            (15, True      and True      and True)         : ( 0,  0, 0, 0,100, 0)
        }
        for key in result:
            if key[1]:
                return result[key]  

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
    col1, col2 = st.columns(2)
    with col1:
        with st.expander("Dow Jones Prediction", True):
            df = pd.read_csv(r"Code/data/dow_jones_prediction.csv")
            df.set_index("Date", inplace=True)
            df = df.rename(columns={"all-mpnet-base-v2_umap":"Prediction"})
            fig = px.line(df, x=df.index, y=[column for column in df.columns[:2]], title='Dow Jones Prediction', color_discrete_sequence=px.colors.sequential.RdBu)
            # for i in df.columns:
            #     if i != "Dow Jones" and i != "Date" and i != "all-mpnet-base-v2_umap":
            #         fig.update_traces(visible='legendonly', selector=dict(name=i))
            st.plotly_chart(fig, use_container_width=True)
            
            # df_rmse = pd.read_csv("Code/data/model_rmse_scores.csv")
            # fig = px.bar(df_rmse, x="Model Name", y="R-squared", title="R-Sqaured Values for Models",color_discrete_sequence=px.colors.sequential.RdBu)
            # fig.update_xaxes(tickangle=90)
            # fig.update_layout(
            # # set tick mode to array, tickvals to your vals calculated and tick text  to the text genrated
            #     yaxis={"tickmode":"array","tickvals":[0.0, 0.2, 0.4, 0.6, 0.8, 1.0], "ticktext":["0.0", "0.2", "0.4", "0.6","0.8", "1.0"]}
            #     )
            # st.plotly_chart(fig, use_container_width=True)
            
            # fig = px.bar(df_rmse, x="Model Name", y="RMSE", title="RMSE Values for Models", color_discrete_sequence=px.colors.sequential.RdBu)
            # fig.update_xaxes(tickangle=90)
            # st.plotly_chart(fig, use_container_width=True)
            
            st.error("💡 Data used for training the models: https://economictimes.indiatimes.com/archive/year-2019.cms")
            Risking_should=1
            Risking = st.slider("Choose your Risklevel", min_value=1, max_value=15)
            # if Risking_should != Risking:
                
                
            # st.subheader("Best model 👑")
            # # name
            # st.write("BERTOPIC (all-mpnet-base-v2_umap)")
            # rsme
            # rmse = df_rmse[df_rmse["Model Name"] == "all-mpnet-base-v2_umap"]["RMSE"].iloc[0]  # Extract the first value from the Series
            # st.write(f'RMSE: {format_euro(rmse)[:-1]}')
            # # accuracy
            # r_squared_value = df_rmse[df_rmse["Model Name"] == "all-mpnet-base-v2_umap"]["R-squared"].iloc[0]  # Extract the first value from the Series
            # accuracy_percentage = r_squared_value * 100
            # st.write(f'Accuracy: {accuracy_percentage:.2f} %')
            # idea behind the model
            # st.write("Idea: Unsupervised topic generation by clustering similar document and similarity calculation")
        with st.expander("📈 Get your Stocks:", True):
            st.session_state.logged_in = True
            st.empty()
            col11, col22 = st.columns(2)
            with col11:
                query_stock_string = st.text_input("Enter a company name")
                query_stock_region = st.selectbox("Select a region", ["US", "BR", "AU", "CA", "FR", "DE", "HK", "IN", "ES", "GB", "SG"])
            with col22:
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
    with col2:      
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