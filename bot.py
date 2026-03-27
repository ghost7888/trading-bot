from flask import Flask, request
from binance.client import Client
import os

app = Flask(__name__)

# GET API KEYS FROM RAILWAY
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# USE TESTNET (IMPORTANT)
client = Client(API_KEY, API_SECRET)
client.API_URL = 'https://testnet.binance.vision/api'

@app.route('/')
def home():
    return "Bot is running!"

# ✅ THIS IS THE IMPORTANT PART (WEBHOOK ROUTE)
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("Received:", data)

    symbol = data.get("symbol")
    side = data.get("side").upper()
    qty = float(data.get("qty"))

    if side == "BUY":
        order = client.order_market_buy(
            symbol=symbol,
            quantity=qty
        )
    elif side == "SELL":
        order = client.order_market_sell(
            symbol=symbol,
            quantity=qty
        )

    return {"status": "success"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
