
from kiteconnect import KiteConnect
import webbrowser
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("Z_API_KEY")
api_secret = os.getenv("Z_API_SECRET")

kite = KiteConnect(api_key=api_key)
login_url = kite.login_url()
print("🔗 Login to Zerodha using this URL:")
print(login_url)
webbrowser.open(login_url)

request_token = input("Paste the request_token from URL after login: ")

data = kite.generate_session(request_token, api_secret=api_secret)
access_token = data["access_token"]
print("✅ Access Token:", access_token)
