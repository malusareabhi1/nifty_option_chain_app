
import streamlit as st
from kiteconnect import KiteConnect
import pandas as pd
import os
from dotenv import load_dotenv

st.set_page_config(page_title="NIFTY Option Chain Viewer", layout="wide")
st.title("📈 Live NIFTY Option Chain – Zerodha API")

load_dotenv()

api_key = os.getenv("Z_API_KEY")
st.text_input("📎 API Key", value=api_key, disabled=True)
access_token_input = st.text_input("🔐 Enter Access Token (required daily)", type="password")

if not access_token_input:
    st.warning("Please enter a valid access token to fetch option chain.")
    st.stop()

kite = KiteConnect(api_key=api_key)

try:
    kite.set_access_token(access_token_input)
    user = kite.profile()
    st.success(f"✅ Logged in as {user['user_name']}")
except Exception as e:
    st.error("❌ Invalid or expired access token.")
    st.stop()

@st.cache_data(ttl=3600)
def get_instruments():
    return pd.DataFrame(kite.instruments("NFO"))

instruments = get_instruments()

nifty_options = instruments[
    (instruments['name'] == 'NIFTY') & (instruments['segment'] == 'NFO-OPT')
]

expiries = sorted(nifty_options['expiry'].unique())
selected_expiry = st.selectbox("📅 Select Expiry Date", expiries)

filtered = nifty_options[nifty_options['expiry'] == selected_expiry]
option_df = filtered[['instrument_token', 'tradingsymbol', 'strike', 'instrument_type']].copy()

ltp_dict = kite.ltp(option_df['instrument_token'].tolist())
option_df['ltp'] = option_df['instrument_token'].map(lambda x: ltp_dict.get(x, {}).get('last_price'))

chain = option_df.pivot_table(index='strike', columns='instrument_type', values='ltp').reset_index()
chain = chain.rename(columns={'CE': 'Call LTP', 'PE': 'Put LTP'}).sort_values('strike')

st.dataframe(chain, use_container_width=True)
