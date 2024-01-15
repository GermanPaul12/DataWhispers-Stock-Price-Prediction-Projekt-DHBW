import pandas as pd
import streamlit as st
import time
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from datetime import datetime, timedelta

# def getDriver():
#     user_agent = "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html)"  # Google Bot User Agent
#     user_agent="Code\data\chromedriver.exe"
#     options = webdriver.ChromeOptions()
#     options.add_argument('--headless')
#     options.add_argument(f'user-agent={user_agent}')
#     options.add_argument('--no-sandbox')
#     options.add_argument('—-disable-extensions')
#     driver = webdriver.Chrome(options=options)
    
#     return driver

# def getDataFrame(Elemente):
#     Kurse=Elemente.split("\n")[1:-1]
#     coloumnNames=[x for x in Kurse.pop(0).split()]
#     coloumnNames.remove("Relation")
#     dat=[x.strip().split() for x in Kurse]
#     data=[]
#     DATEN=[]
#     for x in range(0,len(dat)-1,2):
#         data.append(dat[x]+dat[x+1])
#     for x in data:
#         DATEN.append([" ".join(x[:-7])] + x[-7:-3] +[x[-3] +" "+ x[-2]] + [x[-1]])
#     return pd.DataFrame(columns=coloumnNames, data=DATEN)

# def Dax_Scrapping():
#     url="https://www.tagesschau.de/wirtschaft/boersenkurse/dax-index-846900/"

#     driver=getDriver()
#     driver.get(url)
#     element=driver.find_element(By.XPATH,"/html/body")
#     Kurse = element.text.split("Wertpapiere im DAX ® (40)")[1].split("Die Daten werden")[0]
#     driver.quit()
#     return getDataFrame(Kurse)

url="https://www.tagesschau.de/wirtschaft/boersenkurse/dax-index-846900/"
df = pd.read_html(url)[-1].drop(columns="Relation")

st.title("Es werden hier die aktuelle Daxkurse angezeigt!")
st.write("\n")
randint = np.random.randint(1,1000)

NOW = datetime.now()
Heute, Stunde, Minute = NOW.date(),NOW.hour, NOW.minute
with st.spinner("Wait for it ..."):
    if not os.path.isfile(f"{Heute}_{Stunde}_{Minute}.csv"):
        st.dataframe(df)
        df.to_csv(f"Code/data/dax_data/{Heute}_{Stunde}_{Minute}.csv", encoding="utf-8")
    else:
        df=pd.read_csv(f"{Heute}_{Stunde}_{Minute}.csv",index_col=0,encoding="utf-8")
        st.dataframe(df)
time.sleep(randint + 600*5)
st.experimental_rerun()

