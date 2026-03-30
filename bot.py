from flask import Flask, request
from binance.client import Client
import os

app = Flask(__name__)

# ================= GET API KEYS =================
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# ================= CONNECT TO BINANCE TESTNET =================
try:
    client = Client(API_KEY, API_SECRET, testnet=True)
    client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"
    print("✅ Binance TESTNET connected")
except Exception as e:
    client = None
    print("❌ Binance connection failed:", e)

# ================= HOME ROUTE =================
@app.route("/")
def home():
    return "Bot is running!"

# ================= WEBHOOK ROUTE =================
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("📩 Received:", data)

    if client is None:
        return {"error": "Binance not connected"}

    try:
        symbol = data["symbol"]
        side = data["side"].upper()   # BUY / SELL
        qty = float(data["qty"])
        tp = float(data["tp"])
        sl = float(data["sl"])

        # ================= MARKET ORDER =================
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=qty
        )

        print("✅ Market order placed:", order)

        # ================= TAKE PROFIT =================
        if side == "BUY":
            tp_side = "SELL"
            sl_side = "SELL"
        else:
            tp_side = "BUY"
            sl_side = "BUY"

        client.futures_create_order(
            symbol=symbol,
            side=tp_side,
            type="TAKE_PROFIT_MARKET",
            stopPrice=tp,
            closePosition=True
        )

        client.futures_create_order(
            symbol=symbol,
            side=sl_side,
            type="STOP_MARKET",
            stopPrice=sl,
            closePosition=True
        )

        print("🎯 TP & SL set")

        return {"status": "order + tp/sl placed"}

    except Exception as e:
        print("❌ Order error:", e)
        return {"error": str(e)}

# ================= RUN APP =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
