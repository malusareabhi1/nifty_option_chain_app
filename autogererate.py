
import streamlit as st
from kiteconnect import KiteConnect
import os
from dotenv import load_dotenv
import webbrowser
from datetime import datetime

st.set_page_config(page_title="Zerodha Token Manager", layout="centered")
st.title("🔐 Zerodha Access Token Manager")

# Load current environment
load_dotenv()
api_key = os.getenv("Z_API_KEY", "")
api_secret = os.getenv("Z_API_SECRET", "")
existing_token = os.getenv("Z_ACCESS_TOKEN", "")

# Step 1: Show API info
st.subheader("Step 1: API Credentials")
api_key = st.text_input("API Key", api_key)
api_secret = st.text_input("API Secret", api_secret, type="password")

if st.button("🔗 Open Zerodha Login URL"):
    kite = KiteConnect(api_key=api_key)
    login_url = kite.login_url()
    webbrowser.open_new_tab(login_url)
    st.info("After login, copy the `request_token` from the redirected URL.")

# Step 2: Request Token
st.subheader("Step 2: Enter Request Token")
request_token = st.text_input("Paste request_token here")

if st.button("⚙️ Generate and Save Access Token"):
    try:
        kite = KiteConnect(api_key=api_key)
        session = kite.generate_session(request_token, api_secret=api_secret)
        access_token = session["access_token"]
        st.success("✅ Access Token Generated Successfully!")

        # Save to .env
        env_lines = []
        env_keys = {"Z_API_KEY": api_key, "Z_API_SECRET": api_secret, "Z_ACCESS_TOKEN": access_token}

        if os.path.exists(".env"):
            with open(".env", "r") as f:
                lines = f.readlines()
            for line in lines:
                key = line.strip().split("=")[0]
                if key in env_keys:
                    env_lines.append(f"{key}={env_keys[key]}
")
                    env_keys.pop(key)
                else:
                    env_lines.append(line)
        else:
            env_lines = []

        for k, v in env_keys.items():
            env_lines.append(f"{k}={v}
")

        with open(".env", "w") as f:
            f.writelines(env_lines)

        st.info("💾 .env updated with new access token.")

    except Exception as e:
        st.error(f"❌ Failed to generate token: {str(e)}")

# Token Status
st.subheader("🕒 Token Status")
if existing_token:
    try:
        kite = KiteConnect(api_key=api_key)
        kite.set_access_token(existing_token)
        profile = kite.profile()
        st.success(f"✅ Token is valid. Logged in as: {profile['user_name']}")
        st.caption(f"🗓️ Note: Zerodha tokens expire every day at ~6:00 AM IST.")
    except:
        st.error("❌ Existing token is invalid or expired. Please generate a new one.")
else:
    st.warning("⚠️ No access token found in `.env`. Please generate one.")
