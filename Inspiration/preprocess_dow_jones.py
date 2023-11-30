import pandas as pd

data = pd.read_csv('INDEX_US_DOW JONES GLOBAL_DJIA.csv')
data['Date'] = pd.to_datetime(data['Date'])
data = data.set_index('Date').sort_index()
data.head()

data["Open"] = data["Open"].str.replace(',', '').astype(float)
data["High"] = data["High"].str.replace(',', '').astype(float)
data["Low"] = data["Low"].str.replace(',', '').astype(float)
data["Close"] = data["Close"].str.replace(',', '').astype(float)

data.to_csv('dow_jones_preprocessed.csv')
