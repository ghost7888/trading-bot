from flask import Flask, request, jsonify
from binance.client import Client
import os

app = Flask(__name__)

# 🔐 Get API keys from Railway (NOT hardcoded)
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# Connect to Binance TESTNET
client = Client(API_KEY, API_SECRET)

client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        print("Received:", data)

        symbol = data['symbol']
        side = data['side'].upper()
        qty = float(data['qty'])
        tp = float(data['tp'])
        sl = float(data['sl'])

        # 1️⃣ MARKET ENTRY
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type='MARKET',
            quantity=qty
        )

        # 2️⃣ TAKE PROFIT
        client.futures_create_order(
            symbol=symbol,
            side='SELL' if side == 'BUY' else 'BUY',
            type='TAKE_PROFIT_MARKET',
            stopPrice=tp,
            closePosition=True
        )

        # 3️⃣ STOP LOSS
        client.futures_create_order(
            symbol=symbol,
            side='SELL' if side == 'BUY' else 'BUY',
            type='STOP_MARKET',
            stopPrice=sl,
            closePosition=True
        )

        return jsonify({"status": "success"})

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"status": "error", "message": str(e)})

# Railway needs this format
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
