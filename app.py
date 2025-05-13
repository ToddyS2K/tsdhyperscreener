import streamlit as st
import requests
import pandas as pd

# Titolo app
st.title("Crypto Screener - Volume & Breakout Watch")

# Scarica i dati da CoinGecko
url = "https://api.coingecko.com/api/v3/coins/markets"
params = {
    "vs_currency": "usd",
    "order": "volume_desc",
    "per_page": 50,
    "page": 1,
    "price_change_percentage": "1h,24h"
}
res = requests.get(url, params=params)
data = res.json()

# Trasformazione in DataFrame
df = pd.DataFrame([{
    "Name": c["name"],
    "Symbol": c["symbol"].upper(),
    "Price (USD)": c["current_price"],
    "Volume (24h)": c["total_volume"],
    "Change 1h (%)": round(c["price_change_percentage_1h_in_currency"] or 0, 2),
    "Change 24h (%)": round(c["price_change_percentage_24h_in_currency"] or 0, 2),
} for c in data])

# Filtra coin con variazione 1h < ±2% (prezzo stabile)
stable = df[abs(df["Change 1h (%)"]) < 2]

# Mostra tutto e breakout candidate
st.subheader("Tutte le Top 50 per Volume")
st.dataframe(df)

st.subheader("Possibili Coin in Accumulo (1h ±2%)")
st.dataframe(stable)
