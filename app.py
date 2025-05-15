import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Crypto Screener", layout="wide")
st.title("Crypto Screener - Volume & Breakout Watch")

# === Step 1: Get Data from CoinGecko ===
url = "https://api.coingecko.com/api/v3/coins/markets"
params = {
    "vs_currency": "usd",
    "order": "volume_desc",
    "per_page": 50,
    "page": 1,
    "price_change_percentage": "1h,24h"
}

try:
    res = requests.get(url, params=params)
    data = res.json()
    if isinstance(data, list):
        df = pd.DataFrame([{
            "Name": c.get("name", ""),
            "Symbol": c.get("symbol", "").upper(),
            "Price (USD)": c.get("current_price", 0),
            "Volume (24h)": c.get("total_volume", 0),
            "Change 1h (%)": round(c.get("price_change_percentage_1h_in_currency", 0) or 0, 2),
            "Change 24h (%)": round(c.get("price_change_percentage_24h_in_currency", 0) or 0, 2),
        } for c in data])
    else:
        st.error("Errore: la risposta dell'API non è una lista come previsto.")
        st.stop()
except Exception as e:
    st.error(f"Errore nella trasformazione dei dati: {e}")
    st.stop()

# Filtra coin con variazione 1h < ±2% (prezzo stabile)
stable = df[abs(df["Change 1h (%)"]) < 2]

# Mostra tutto e breakout candidate
st.subheader("Tutte le Top 50 per Volume")
st.dataframe(df.sort_values("Volume (24h)", ascending=False), use_container_width=True)

st.subheader("Possibili Coin in Fase di Accumulo (1h ±2%)")
st.dataframe(stable.sort_values("Change 24h (%)", ascending=False), use_container_width=True)
