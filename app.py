from flask import Flask, request, jsonify
import os
from pybit.unified_trading import HTTP

app = Flask(__name__)

API_KEY = os.getenv("BYBIT_API_KEY")
API_SECRET = os.getenv("BYBIT_API_SECRET")

session = HTTP(
    testnet=True,
    api_key=API_KEY,
    api_secret=API_SECRET
)

@app.route("/")
def home():
    return "Bot is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    try:
        symbol = data["symbol"]
        side = data["side"]
        qty = float(data["qty"])

        order_side = "Buy" if side == "buy" else "Sell"

        response = session.place_order(
            category="linear",
            symbol=symbol,
            side=order_side,
            orderType="Market",
            qty=qty,
            timeInForce="GoodTillCancel"
        )

        print("ORDER:", response)

        return jsonify({"status": "success"})

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500
