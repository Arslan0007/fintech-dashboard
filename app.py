from flask import Flask, jsonify
import random
import datetime

app = Flask(__name__)

# --- HELPER FUNCTIONS ---
def generate_market_data(base_price, volatility):
    price = round(random.uniform(base_price * 0.95, base_price * 1.05), 2)
    change = round(random.uniform(-volatility, volatility), 2)
    return price, change

def get_signal(change):
    if change > 1.2: return "STRONG BUY 🚀"
    elif change > 0.3: return "BUY"
    elif change < -1.2: return "STRONG SELL 📉"
    elif change < -0.3: return "SELL"
    else: return "HOLD ✋"

def get_color(change):
    return "#00ff00" if change >= 0 else "#ff4444"

# --- ROUTES ---

@app.route('/')
def home():
    html_content = """
    <html>
        <head>
            <title>ProTrade Terminal v2.0</title>
            <script>
                function updatePrices() {
                    fetch('/api/data')
                        .then(response => response.json())
                        .then(data => {
                            updateCard('aapl', data.aapl);
                            updateCard('tsla', data.tsla);
                            updateCard('googl', data.googl);
                            updateCard('btc', data.btc);
                            updateCard('eth', data.eth);
                            
                            document.getElementById('risk_alert').innerHTML = data.risk_alert;
                        });
                }
                
                function updateCard(id, data) {
                    document.getElementById(id + '_price').innerText = '$' + data.price;
                    document.getElementById(id + '_change').innerText = data.change + '%';
                    document.getElementById(id + '_change').style.color = data.color;
                    document.getElementById(id + '_msg').innerText = data.signal;
                }

                setInterval(updatePrices, 2000);
            </script>
            <style>
                body { font-family: 'Consolas', 'Monaco', monospace; background-color: #050505; color: #e0e0e0; margin: 0; padding: 20px; text-align: center; }
                
                .header { border-bottom: 2px solid #333; padding-bottom: 20px; margin-bottom: 30px; }
                h1 { margin: 0; letter-spacing: 3px; color: #fff; }
                .sub-header { color: #666; font-size: 12px; margin-top: 5px; }

                .container { display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; max-width: 1200px; margin: 0 auto; }
                
                .card { background: #111; border: 1px solid #333; padding: 15px; width: 200px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.5); transition: transform 0.2s; }
                .card:hover { transform: scale(1.02); border-color: #555; }
                
                h2 { color: #888; font-size: 14px; margin: 0 0 10px 0; }
                .price { font-size: 28px; font-weight: bold; margin: 10px 0; }
                .signal-box { background: #1a1a1a; border: 1px solid #333; padding: 5px; margin-top: 10px; font-size: 11px; color: #aaa; }
                
                .crypto-card { border-top: 3px solid #f7931a; } /* Bitcoin Orange */
                .eth-card { border-top: 3px solid #627eea; } /* Ethereum Blue */
                .stock-card { border-top: 3px solid #00ff00; } /* Stock Green */

                .alert { background-color: #500000; color: #ff9999; border: 1px solid #ff0000; padding: 10px; font-weight: bold; animation: flash 1s infinite; margin-bottom: 20px; }
                @keyframes flash { 0% { opacity: 1; } 50% { opacity: 0.6; } 100% { opacity: 1; } }
                
                .ticker-wrap { position: fixed; bottom: 30px; width: 100%; background-color: #111; border-top: 1px solid #333; height: 30px; line-height: 30px; left: 0; }
                .ticker { display: inline-block; white-space: nowrap; animation: ticker 25s linear infinite; color: #00ff00; font-size: 14px; }
                @keyframes ticker { 0% { transform: translate3d(100%, 0, 0); } 100% { transform: translate3d(-100%, 0, 0); } }
                
                .disclaimer { position: fixed; bottom: 5px; width: 100%; font-size: 10px; color: #444; text-align: center; left: 0; background: #000; }
            </style>
        </head>
        <body>
            <div id="risk_alert"></div>
            
            <div class="header">
                <h1>📈 ALGO-TRADER PRO</h1>
                <div class="sub-header">INSTITUTIONAL GRADE MARKET SIMULATOR</div>
            </div>
            
            <div class="container">
                <div class="card stock-card">
                    <h2>APPLE (AAPL)</h2>
                    <div id="aapl_price" class="price">...</div>
                    <div id="aapl_change">...</div>
                    <div class="signal-box">SIGNAL: <b id="aapl_msg">...</b></div>
                </div>

                <div class="card stock-card">
                    <h2>TESLA (TSLA)</h2>
                    <div id="tsla_price" class="price">...</div>
                    <div id="tsla_change">...</div>
                    <div class="signal-box">SIGNAL: <b id="tsla_msg">...</b></div>
                </div>

                <div class="card stock-card">
                    <h2>GOOGLE (GOOGL)</h2>
                    <div id="googl_price" class="price">...</div>
                    <div id="googl_change">...</div>
                    <div class="signal-box">SIGNAL: <b id="googl_msg">...</b></div>
                </div>

                <div class="card crypto-card">
                    <h2>BITCOIN (BTC)</h2>
                    <div id="btc_price" class="price">...</div>
                    <div id="btc_change">...</div>
                    <div class="signal-box">SIGNAL: <b id="btc_msg">...</b></div>
                </div>

                <div class="card eth-card">
                    <h2>ETHEREUM (ETH)</h2>
                    <div id="eth_price" class="price">...</div>
                    <div id="eth_change">...</div>
                    <div class="signal-box">SIGNAL: <b id="eth_msg">...</b></div>
                </div>
            </div>

            <div class="ticker-wrap">
                <div class="ticker">📰 NEWS: TESLA ANNOUNCES NEW AI ROBOT +++ BITCOIN HALVING EVENT APPROACHING +++ GOOGLE EARNINGS BEAT EXPECTATIONS +++ ETHEREUM GAS FEES DROP TO RECORD LOWS</div>
            </div>

            <div class="disclaimer">
                MIT LICENSE | DISCLAIMER: This is a simulation for portfolio demonstration only. NOT financial advice.
            </div>
        </body>
    </html>
    """
    return html_content

@app.route('/api/data')
def get_data():
    # Generate data for all assets
    aapl_p, aapl_c = generate_market_data(170, 2.0)
    tsla_p, tsla_c = generate_market_data(240, 4.0) # Tesla is more volatile
    googl_p, googl_c = generate_market_data(135, 1.5)
    btc_p, btc_c = generate_market_data(30000, 5.0)
    eth_p, eth_c = generate_market_data(1800, 4.0)

    # Risk Logic
    risk_alert = ""
    if btc_c < -2.5 or tsla_c < -3.0:
        risk_alert = """<div class="alert">⚠️ MARKETS FLASHING RED: HIGH VOLATILITY DETECTED.</div>"""

    return jsonify({
        'aapl': {'price': aapl_p, 'change': aapl_c, 'color': get_color(aapl_c), 'signal': get_signal(aapl_c)},
        'tsla': {'price': tsla_p, 'change': tsla_c, 'color': get_color(tsla_c), 'signal': get_signal(tsla_c)},
        'googl': {'price': googl_p, 'change': googl_c, 'color': get_color(googl_c), 'signal': get_signal(googl_c)},
        'btc': {'price': btc_p, 'change': btc_c, 'color': get_color(btc_c), 'signal': get_signal(btc_c)},
        'eth': {'price': eth_p, 'change': eth_c, 'color': get_color(eth_c), 'signal': get_signal(eth_c)},
        'risk_alert': risk_alert
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)