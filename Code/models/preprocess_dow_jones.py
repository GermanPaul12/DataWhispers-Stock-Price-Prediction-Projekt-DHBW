import pandas as pd

data = pd.read_csv('Code/data/Dow_Jones.csv')
data['Date'] = pd.to_datetime(data['Date'])
data = data.set_index('Date').sort_index()
print(data.head())

data["Open"] = data["Open"].astype(float)
data["High"] = data["High"].astype(float)
data["Low"] = data["Low"].astype(float)
data["Close"] = data["Close"].astype(float)

data.to_csv('Code/data/dow_jones_preprocessed.csv')
