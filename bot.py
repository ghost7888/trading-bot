from flask import Flask, request, jsonify
import os
from pybit.unified_trading import HTTP

app = Flask(__name__)

# Load API keys
API_KEY = os.getenv("BYBIT_API_KEY")
API_SECRET = os.getenv("BYBIT_API_SECRET")

# Connect to Bybit Testnet
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
        symbol = data.get("symbol", "BTCUSDT")
        side = data.get("side")
        qty = float(data.get("qty", 0.001))

        if side not in ["buy", "sell"]:
            return jsonify({"error": "Invalid side"}), 400

        order_side = "Buy" if side == "buy" else "Sell"

        response = session.place_order(
            category="linear",
            symbol=symbol,
            side=order_side,
            orderType="Market",
            qty=qty,
            timeInForce="GoodTillCancel"
        )

        print("ORDER RESPONSE:", response)

        return jsonify({"status": "order placed", "response": response})

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
