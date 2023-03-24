
from datetime import datetime
from hmac import HMAC
from hashlib import sha256
import time
import json
import requests
import config
import hashlib
import json
import hmac


class Bybit():
    def __init__(self, api_key,  secret_key, recv_window='20000'):
        self.api_key = api_key
        self.secret_key = secret_key
        self.recv_window = recv_window

    def signature(self, params):
        timeStamp = str(int(time.time() * 1000))
        param_str = str(timeStamp) + self.api_key + \
            self.recv_window + json.dumps(params)

        hash = hmac.new(bytes(self.secret_key, "utf-8"),
                        param_str.encode("utf-8"), hashlib.sha256)
        signature = hash.hexdigest()
        headers = {
            'X-BAPI-API-KEY': self.api_key,
            'X-BAPI-SIGN': signature,
            'X-BAPI-SIGN-TYPE': '2',
            'X-BAPI-TIMESTAMP': str(timeStamp),
            'X-BAPI-RECV-WINDOW': self.recv_window,
            'Content-Type': 'application/json'
        }

        return headers

    def buy_limit(self, symbol, qty, price, tp='', sl=''):
        params = {
            "symbol": symbol,
            'category': 'linear',
            "side": "Buy",
            "order_type": "Limit",
            "qty": qty,
            'positionIdx': 1,
            "price": price,
            'takeProfit': tp,
            'stopLoss': sl,
            "api_key": self.api_key, }

        headers = self.signature(params)

        url = "https://api.bybit.com/v5/order/create"
        response = requests.request(
            "POST", url, headers=headers, data=json.dumps(params))

        return response.json()

    def sell_limit(self, symbol, qty, price, tp='', sl=''):
        params = {
            "symbol": symbol,
            'category': 'linear',
            "side": "Sell",
            "order_type": "Limit",
            "qty": qty,
            'positionIdx': 2,
            "price": price,
            'takeProfit': tp,
            'stopLoss': sl,
            "api_key": self.api_key, }

        headers = self.signature(params)

        url = "https://api.bybit.com/v5/order/create"
        response = requests.request(
            "POST", url, headers=headers, data=json.dumps(params))

        return response.json()

    def cancel_order(self, symbol, orderId):
        params = {
            "category": "linear",
            "symbol": symbol,
            # "orderId": 'null',
            # "orderLinkId": 'null',
            "orderFilter": "Order", }
        timeStamp = str(int(time.time() * 1000))
        param_str = str(timeStamp) + self.api_key + \
            self.recv_window + json.dumps(params)

        hash = hmac.new(bytes(self.secret_key, "utf-8"),
                        param_str.encode("utf-8"), hashlib.sha256)
        signature = hash.hexdigest()
        headers = {
            'X-BAPI-API-KEY': self.api_key,
            'X-BAPI-SIGN': signature,
            'X-BAPI-TIMESTAMP': str(timeStamp),
            'X-BAPI-RECV-WINDOW': self.recv_window,
        }

        url = 'https://api.bybit.com/v5/order/cancel'

        response = requests.request("POST", url, headers=headers, data=params)

        return response.json()

    def instrument_info(self, symbol):
        url = "https://api-testnet.bybit.com/v5/market/instruments-info?category=linear"

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)
        data = response.json()['result']['list']

        for symbol_info in data:
            if symbol_info['symbol'] == symbol:
                leverage_filter = symbol_info['leverageFilter']
                min_leverage = leverage_filter['minLeverage']
                max_leverage = leverage_filter['maxLeverage']
                lotSizeFilter = symbol_info['lotSizeFilter']
                maxOrderQty = lotSizeFilter['maxOrderQty']
                minOrderQty = lotSizeFilter['minOrderQty']
                info = [min_leverage, max_leverage, maxOrderQty, minOrderQty]
                break
            else:
                info = False

        return info


bybit = Bybit(config.api_key, config.api_secret)


# print(bybit.instrument_info())

x = bybit.instrument_info('BTCUSDT')
print(x[0])


# buy_limit = bybit.buy_limit('BTCUSDT', "0.001", '17000')
# print(buy_limit)
# x = buy_limit['result']['orderId']
# print('orderLinkId :', buy_limit['result']['orderLinkId'])

# print(x)

# time.sleep(3)
# cancel_order = bybit.cancel_order(
#     'BTCUSDT', x)
# print(cancel_order)
# sell_limit = bybit.sell_limit('BTCUSDT', "0.001", '40000')
# print(sell_limit)
# print(sell_limit['retMsg'])
