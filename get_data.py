import json
import config
import requests
import hmac
import hashlib
from urllib.parse import urlencode
import time


def get_signature(params, secret_key):
    total_params = urlencode(params)
    signature = hmac.new(
        bytes(secret_key, 'utf-8'),
        msg = bytes(total_params, 'utf-8'),
        digestmod = hashlib.sha256
    ).hexdigest()
    return signature

def SIGNED_REQUEST(method, params, url, key, secret_key):
    headers = {"X-MBX-APIKEY": key}
    signature = get_signature(params, secret_key)
    params["signature"] = signature
    req_url = "https://testnet.binance.vision" + url
    if method == "POST":
        response = requests.post(req_url, params=params, headers=headers)
    elif method == "GET":
        response = requests.get(req_url, params=params, headers=headers)
    return response.json()


ts = int(round(time.time()*1000))
SPOT_KEY = config.SPOT_KEY
SPOT_SECRET = config.SPOT_SECRET
headers = {"X-MBX-APIKEY": SPOT_KEY}


# pull the price of ETH-USDT
print("Price of ETH-USDT: ")
price_params = {"symbol": "ETHUSDT"}
price = requests.get("https://api.binance.com/api/v3/ticker/price", params=price_params)
print(price.json())


print("ETH before trade: ")
# get user data before exchange (Spot)
time_params = {"timestamp": ts}
user_data = SIGNED_REQUEST("GET", time_params, "/api/v3/account", SPOT_KEY, SPOT_SECRET)
print(user_data["balances"][3])
print(user_data["balances"][6])


print("----------------------------------------------------")

print("Buy 0.1 ETH with USDT:")
ts = int(round(time.time()*1000))
order_params = {"symbol": "ETHUSDT", "side": "BUY", "type": "MARKET", "quantity": 0.1, "timestamp": ts}
order_response = SIGNED_REQUEST("POST", order_params, "/api/v3/order", SPOT_KEY, SPOT_SECRET)
print(order_response)

print("----------------------------------------------------")

print("ETH after trade:")
ts = int(round(time.time()*1000))
time_params = {"timestamp": ts}
user_data = SIGNED_REQUEST("GET", time_params, "/api/v3/account", SPOT_KEY, SPOT_SECRET)
print(user_data["balances"][3])
print(user_data["balances"][6])
