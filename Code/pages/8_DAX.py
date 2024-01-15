import pandas as pd
import streamlit as st
import time
import numpy as np
import os
from datetime import datetime, timedelta

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

