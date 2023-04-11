
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
import requests
import json
from datetime import timedelta
import numpy as np
import pandas as pd
from datetime import datetime
import os
# from IPython.display import clear_output
# import local_settings
import hmac
import hashlib

class Bybit():
    def __init__(self, api_key,  secret_key, recv_window='20000'):
        self.api_key = api_key
        self.secret_key = secret_key
        self.recv_window = recv_window

    def signature(self, params , defrent_params_str = False):
        timeStamp = str(int(time.time() * 1000))
        param_str = str(timeStamp) + self.api_key + \
            self.recv_window + json.dumps(params)
        if defrent_params_str :
            params_str = '&'.join([f"{k}={v}" for k, v in params.items()])
            param_str = f'{timeStamp}{self.api_key}{self.recv_window}{params_str}'
        

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
            "api_key": self.api_key,}

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
    # TODO cancel order not work

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
    
    def leverage(self , symbol ,buyLeverage ,sellLeverage ):
        params = {
        "symbol": symbol,
        'category': 'linear',
        'buyLeverage' : buyLeverage , 
        'sellLeverage': sellLeverage  , 
        "api_key": self.api_key,}
        
        url = 'https://api.bybit.com/v5/position/set-leverage'
        headers = self.signature(params)
        response = requests.request(
            "POST", url, headers=headers, data=json.dumps(params))      
        return response.json()  

    def open_position_tp_sl(self , symbol ,takeProfit ,stopLoss , positionIdx , tpSize='', slSize = ''):
        '''
        set tp and sl for open position
        Buy side : positionIdx = 1 
        Sell side : positionIdx = 1 
        '''
        params = {
        "symbol": symbol,
        'category': 'linear',
        'takeProfit' : takeProfit , 
        'stopLoss': stopLoss  , 
        'positionIdx': positionIdx ,
        'tpSize': tpSize,
        'slSize' : slSize,
        "api_key": self.api_key,}
        
        url = 'https://api.bybit.com/v5/position/trading-stop'
        headers = self.signature(params)
        response = requests.request(
            "POST", url, headers=headers, data=json.dumps(params))      
        return response.json()  

        
    def instrument_info(self, symbol):
        url = "https://api-testnet.bybit.com/v5/market/instruments-info?category=linear"

        params = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=params)
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

    def get_position_info(self, symbol):
        params = {'category': 'linear',
                    "symbol":symbol}
    
        
        url = "https://api.bybit.com/v5/position/list"
        

        header = self.signature(params , True)
        response = requests.get(url = url,headers=header , params=params)
        data = response.json()['result']['list']
        long = data[0]
        short = data[1]
        
        if int(float(long['avgPrice'])) != 0 :
            symbol = long['symbol']
            side = long['side']
            size = long['size']
            avgPrice = long['avgPrice']
            leverage = long['leverage']
            liqPrice = long['liqPrice']
            takeProfit = long['takeProfit']
            stopLoss = long['stopLoss']
            unrealisedPnl = long['unrealisedPnl']

            long_info = [symbol , side , size ,avgPrice   , leverage   , liqPrice , takeProfit, stopLoss, unrealisedPnl]
        else : 
            long_info = False

        if int(float(short['avgPrice'])) != 0 :
            symbol = short['symbol']
            side = short['side']
            size = short['size']
            avgPrice = short['avgPrice']
            leverage = short['leverage']
            liqPrice = short['liqPrice']
            takeProfit = short['takeProfit']
            stopLoss = short['stopLoss']
            unrealisedPnl = short['unrealisedPnl']

            short_info = [symbol , side , size ,avgPrice   , leverage   , liqPrice , takeProfit, stopLoss, unrealisedPnl]
        else : 
            short_info = False
        return long_info , short_info
    
    def last_price(self , symbol):
        timeStamp = str(int(time.time() * 1000))
        
        url = f'https://api.bybit.com/v5/market/kline?category=linear&symbol={symbol}&interval=1'
        response = requests.request('GET' , url)
        df = pd.DataFrame(response.json()['result']['list'])
        return df.iloc[0][4]

