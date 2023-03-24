

# How to Use the Bybit API with this Program

To start using the Binance API with this program, you need to provide your API key and secret key to the Bybit class. Here's an example of how to do it :

'''
import config
from main import Bybit


bybit = Bybit(config.api_key, config.api_secret)

'''
After you have provided the API and secret key, you can execute various actions using the Binance API. Here are a few examples:

# Open a long limit order


```

buy_limit = bybit.buy_limit('BTCUSDT', "0.001", '17000')
print('result :' , buy_limit)

```
The above code will open a long limit order for 0.001 BTC at a price of 17000 USDT.


output :

```
result : {'retCode': 0, 'retMsg': 'OK', 'result': {'orderId': 'e61440fd-8e01-4aec-8730-1fb2e0b954fc', 'orderLinkId': ''}, 'retExtInfo': {}, 'time': 1679670075978}
```
# Open a short limit order

```

sell_limit = bybit.sell_limit('BTCUSDT', "0.001", '40000')
print('result :' , sell_limit)

```
The above code will open a short limit order for 0.001 BTC at a price of 40000 USDT.



output :

```
result : {'retCode': 0, 'retMsg': 'OK', 'result': {'orderId': 'd6768128-4bb7-4b58-902a-8c134df66d96', 'orderLinkId': ''}, 'retExtInfo': {}, 'time': 1679671142553}
```

# Check symbol existence and get instrument information

```
BTC = bybit.instrument_info('BTCUSDT')

if BTC:
    print(
        f' min_leverage : {BTC[0]} \n max_leverage :{ BTC[1]} \n maxOrderQty : {BTC[2]} \n maxOrderQty : {BTC[3]}')
else:
    print(BTC)

```


The above code will check if the symbol 'BTCUSDT' exists on the Binance platform and retrieve its instrument information, including minimum leverage, maximum leverage, maximum order quantity, and price tick size. If the symbol exists, the output will be printed to the console. If it doesn't exist, the instrument_info function will return False.


output :

```
 min_leverage : 1
 max_leverage :100.00
 maxOrderQty : 100.000
 maxOrderQty : 0.001
```