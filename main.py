from private.credentials import *
from binance.spot import Spot

client = Spot(key=api_key, secret=secret_key, base_url="https://testnet.binance.vision")

print(client.time())
# Get klines of BTCUSDT at 1m interval
print(client.klines("ETHUSDT", "1m"))
print(client.avg_price("ETHUSDT"))

# Get account information
print(client.account())

# Post a new order
params = {
    'symbol': 'BTCUSDT',
    'side': 'SELL',
    'type': 'LIMIT',
    'timeInForce': 'GTC',
    'quantity': 0.002,
    'price': 25000
}

response = client.get_orders("BTCUSDT")
print(response)

response = client.new_order(**params)
print(response)

arg = { "orderId": 1901579 }

#response = client.cancel_order(symbol='BTCUSDT', **arg)
response = client.cancel_open_orders(symbol='BTCUSDT')
print(response)

import plotly.graph_objects as go

import pandas as pd
from datetime import datetime

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')

fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                     open=df['AAPL.Open'],
                                     high=df['AAPL.High'],
                                     low=df['AAPL.Low'],
                                     close=df['AAPL.Close'])])

fig.show()