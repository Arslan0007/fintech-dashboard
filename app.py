from flask import Flask, jsonify
import random
import datetime

app = Flask(__name__)

# 1. The "Page" Route - Loads only ONCE
@app.route('/')
def home():
    html_content = """
    <html>
        <head>
            <title>ProTrade Terminal</title>
            <script>
                // This JavaScript runs in the browser
                function updatePrices() {
                    fetch('/api/data') // Ask server for new numbers
                        .then(response => response.json())
                        .then(data => {
                            // Update Apple
                            document.getElementById('aapl_price').innerText = '$' + data.apple_price;
                            document.getElementById('aapl_change').innerText = data.apple_change + '%';
                            document.getElementById('aapl_change').style.color = data.apple_color;
                            document.getElementById('aapl_msg').innerText = data.apple_signal;

                            // Update Bitcoin
                            document.getElementById('btc_price').innerText = '$' + data.btc_price;
                            document.getElementById('btc_change').innerText = data.btc_change + '%';
                            document.getElementById('btc_change').style.color = data.btc_color;
                            document.getElementById('btc_msg').innerText = data.btc_signal;

                            // Update Alert
                            document.getElementById('risk_alert').innerHTML = data.risk_alert;
                        });
                }
                // Run update every 2000 milliseconds (2 seconds)
                setInterval(updatePrices, 2000);
            </script>
            <style>
                body { font-family: 'Consolas', 'Monaco', monospace; background-color: #000000; color: #e0e0e0; margin: 0; padding: 20px; text-align: center; }
                .container { display: flex; justify-content: center; gap: 40px; margin-top: 30px; flex-wrap: wrap; }
                .card { background: #111; border: 1px solid #333; padding: 20px; width: 320px; border-radius: 8px; box-shadow: 0 0 15px rgba(0,255,0,0.05); }
                h1 { color: #ffffff; letter-spacing: 2px; text-transform: uppercase; border-bottom: 1px solid #333; padding-bottom: 10px; display: inline-block; }
                .price { font-size: 42px; font-weight: bold; margin: 15px 0; }
                .signal-box { background: #222; border: 1px solid #444; padding: 8px; margin-top: 10px; font-size: 12px; color: #aaa; }
                
                /* Animations */
                .alert { background-color: #500000; color: #ff9999; border: 1px solid #ff0000; padding: 10px; font-weight: bold; animation: flash 1s infinite; margin-bottom: 20px; }
                @keyframes flash { 0% { opacity: 1; } 50% { opacity: 0.6; } 100% { opacity: 1; } }
                
                /* Ticker - Runs forever now! */
                .ticker-wrap { position: fixed; bottom: 40px; width: 100%; background-color: #111; border-top: 1px solid #333; border-bottom: 1px solid #333; overflow: hidden; height: 30px; line-height: 30px; }
                .ticker { display: inline-block; white-space: nowrap; animation: ticker 20s linear infinite; color: #00ff00; font-size: 14px; }
                @keyframes ticker { 0% { transform: translate3d(100%, 0, 0); } 100% { transform: translate3d(-100%, 0, 0); } }
                
                .disclaimer { position: fixed; bottom: 5px; width: 100%; font-size: 10px; color: #555; text-align: center; }
            </style>
        </head>
        <body>
            <div id="risk_alert"></div>
            <h1>🏛️ Algo-Trade Execution Engine v1.5</h1>
            
            <div class="container">
                <div class="card">
                    <h2>APPLE INC (AAPL)</h2>
                    <div id="aapl_price" class="price">LOADING...</div>
                    <div id="aapl_change">...</div>
                    <div class="signal-box">SIGNAL: <b id="aapl_msg" style="color: white">WAITING</b></div>
                </div>

                <div class="card">
                    <h2>BITCOIN (BTC-USD)</h2>
                    <div id="btc_price" class="price">LOADING...</div>
                    <div id="btc_change">...</div>
                    <div class="signal-box">SIGNAL: <b id="btc_msg" style="color: white">WAITING</b></div>
                </div>
            </div>

            <div class="ticker-wrap">
                <div class="ticker">📰 NEWS: FED RATE DECISION PENDING +++ BITCOIN VOLATILITY INCREASING +++ TECH SECTOR RALLY CONTINUES +++ OIL PRICES STABLE +++ SYSTEM STATUS: ONLINE</div>
            </div>

            <div class="disclaimer">
                DISCLAIMER: This application is a simulation for educational purposes only. NOT financial advice.
            </div>
        </body>
    </html>
    """
    return html_content

# 2. The "Hidden" API Route - Delivers Raw Data
@app.route('/api/data')
def get_data():
    # Simulation Logic
    apple_price = round(random.uniform(165, 175), 2)
    apple_change = round(random.uniform(-1.5, 1.5), 2)
    btc_price = round(random.uniform(29500, 31500), 2)
    btc_change = round(random.uniform(-3.5, 3.5), 2)

    def get_signal(change):
        if change > 1.0: return "STRONG BUY 🚀"
        elif change > 0.2: return "BUY"
        elif change < -1.0: return "STRONG SELL 📉"
        elif change < -0.2: return "SELL"
        else: return "HOLD ✋"

    def get_color(change):
        return "#00ff00" if change >= 0 else "#ff4444"

    risk_alert = ""
    if btc_change < -2.0:
        risk_alert = """<div class="alert">⚠️ RISK WARNING: HIGH VOLATILITY DETECTED. AUTOMATED HEDGING ACTIVE.</div>"""

    # Return JSON (Data only, no HTML)
    return jsonify({
        'apple_price': apple_price,
        'apple_change': apple_change,
        'apple_color': get_color(apple_change),
        'apple_signal': get_signal(apple_change),
        'btc_price': btc_price,
        'btc_change': btc_change,
        'btc_color': get_color(btc_change),
        'btc_signal': get_signal(btc_change),
        'risk_alert': risk_alert
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)