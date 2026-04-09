from flask import Flask, request
import os
from pybit.unified_trading import HTTP

app = Flask(__name__)

# ================= API KEYS =================
API_KEY = os.getenv("BYBIT_API_KEY")
API_SECRET = os.getenv("BYBIT_API_SECRET")

# ================= BYBIT CONNECTION =================
session = HTTP(
    testnet=True,  # IMPORTANT: keep True for demo
    api_key=API_KEY,
    api_secret=API_SECRET
)

# ================= HOME =================
@app.route('/')
def home():
    return "Bot is running!"

# ================= WEBHOOK =================
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("Received:", data)

    try:
        symbol = data.get("symbol")
        side = data.get("side")
        qty = float(data.get("qty"))
        tp = float(data.get("tp"))
        sl = float(data.get("sl"))

        # Convert to Bybit format
        order_side = "Buy" if side.lower() == "buy" else "Sell"

        response = session.place_order(
            category="linear",  # Futures
            symbol=symbol,
            side=order_side,
            orderType="Market",
            qty=qty,
            takeProfit=tp,
            stopLoss=sl,
            timeInForce="GoodTillCancel"
        )

        print("ORDER RESPONSE:", response)

        return {"status": "success", "response": response}

    except Exception as e:
        print("ERROR:", str(e))
        return {"status": "error", "message": str(e)}

# ================= RUN =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
