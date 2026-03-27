from flask import Flask, request
import os

app = Flask(__name__)

# ✅ NO BINANCE AT START (IMPORTANT)

@app.route('/')
def home():
    return "Bot is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("Received:", data)

    # JUST PRINT FOR NOW (TESTING)
    return {"status": "received"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
