import requests
import hashlib
import hmac
import numpy as np
import time
from datetime import datetime, timedelta
import statistics




API_KEY = 'API_KEY'
API_SECRET = 'API_SECRET'

volatilite = []
# Step 1: Determine yesterday's date
yesterday = datetime.now() - timedelta(days=1)

# Step 2: Make an API request to fetch historical data
symbol = ['BTCEUR', 'TOMOBTC', 'BTCUSDT', 'EURUSDT', 'TOMOUSDT', 'ETHEUR', 'ETHBTC', 'ETHUSDT']

start_time = int(yesterday.timestamp() * 1000)  # Convert to milliseconds
end_time = int(datetime.now().timestamp() * 1000)  # Convert to milliseconds



i = 0
prix = [1.2]
achat = 1
percent = 0
pourcent = 0

z_achatmax = 0
z_vente  = 0
z_vente1 = 0
z_max = 0
z_achat = 29658.73

banque_account =0
total_balance=0
plus_value = 0
quantity = 0

def get_binance_price(symbol):
    base_url = 'https://api.binance.com/api/v3/ticker/price'
    params = {'symbol': symbol}

    response = requests.get(base_url, params=params)
    data = response.json()

    if 'price' in data:
        return float(data['price'])
    else:
        return None

def generate_signature(params):
    query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
    return hmac.new(API_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

def get_server_timestamp():
    endpoint = 'https://api.binance.com/api/v3/time'
    response = requests.get(endpoint)
    data = response.json()
    if 'serverTime' in data:
        return data['serverTime']
    else:
        return None

def get_asset_precision(symbol):
    endpoint = f'https://api.binance.com/api/v3/exchangeInfo?symbol={symbol}'
    response = requests.get(endpoint)
    data = response.json()
    if 'symbols' in data:
        symbols = data['symbols']
        for s in symbols:
            if s['symbol'] == symbol:
                filters = s['filters']
                for f in filters:
                    if f['filterType'] == 'LOT_SIZE':
                        return int(f['stepSize'].index('1') - 1)
    return None

def create_binance_order(symbol, side, quantity):
    server_timestamp = get_server_timestamp()
    if server_timestamp is None:
        print("Impossible d'obtenir l'horodatage du serveur.")
        return

    precision = get_asset_precision(symbol)
    if precision is None:
        print(f"Impossible d'obtenir la précision pour la paire de trading {symbol}.")
        return

    quantity = round(float(quantity), precision)  # Ajuster la précision du montant

    endpoint = 'https://api.binance.com/api/v3/order'
    params = {
        'symbol': symbol,
        'side': side,
        'type': 'MARKET',
        'quantity': quantity,
        'timestamp': server_timestamp
    }
    headers = {
        'X-MBX-APIKEY': API_KEY
    }

    params['signature'] = generate_signature(params)

    response = requests.post(endpoint, params=params, headers=headers)
    data = response.json()

    if 'orderId' in data:
        print(f"Ordre d'achat de {quantity} {symbol} réussi !")
        print("ID de commande :", data['orderId'])
    else:
        print(f"Échec de l'ordre d'achat de {quantity} {symbol} !")
        print("Message d'erreur :", data['msg'])

def vente_binance_order(symbol, side, quantity):
    server_timestamp = get_server_timestamp()
    if server_timestamp is None:
        print("Impossible d'obtenir l'horodatage du serveur.")
        return

    precision = get_asset_precision(symbol)
    if precision is None:
        print(f"Impossible d'obtenir la précision pour la paire de trading {symbol}.")
        return

    quantity = round(float(quantity), precision)  # Ajuster la précision du montant

    endpoint = 'https://api.binance.com/api/v3/order'
    params = {
        'symbol': symbol,
        'side': side,
        'type': 'MARKET',
        'quantity': quantity,
        'timestamp': server_timestamp
    }
    headers = {
        'X-MBX-APIKEY': API_KEY
    }

    params['signature'] = generate_signature(params)

    response = requests.post(endpoint, params=params, headers=headers)
    data = response.json()

    if 'orderId' in data:
        print(f"Ordre de vente de {quantity} {symbol} réussi !")
        print("ID de commande :", data['orderId'])
    else:
        print(f"Échec de l'ordre de vente {quantity} {symbol} !")
        print("Message d'erreur :", data['msg'])

def get_binance_account_balance():
    server_timestamp = get_server_timestamp()
    if server_timestamp is None:
        return None, None

    endpoint = 'https://api.binance.com/api/v3/account'
    params = {
        'timestamp': server_timestamp,
        'recvWindow': 5000
    }
    headers = {
        'X-MBX-APIKEY': API_KEY
    }
    params['signature'] = generate_signature(params)

    response = requests.get(endpoint, params=params, headers=headers)
    data = response.json()

    if 'balances' in data:
        tomo_balance = None
        usdt_balance = None

        for balance in data['balances']:
            if balance['asset'] == 'BTC':
                tomo_balance = float(balance['free']) + float(balance['locked'])
            elif balance['asset'] == 'USDT':
                usdt_balance = float(balance['free']) + float(balance['locked'])

        return tomo_balance, usdt_balance

    return None, None

def volatilites(symbol, start_time, end_time):
    # intervale de temps: 5m 1h 30m
    interval = '30m'
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "startTime": start_time,
        "endTime": end_time
    }

    response = requests.get(url, params=params)
    data = response.json()
    print(data)
    for item in data:
        print(float(item[4]))

    # Step 4: Extract price values for the specified time interval
    price_values = [float(item[4]) for item in data]

    # Step 5: Calculate the standard deviation
    std_dev = statistics.stdev(price_values)

    # Step 6: Print the standard deviation
    print(symbol ,"Volatilité : ", std_dev, "€", ' sur ',interval )
    return std_dev

symbol = 'BTCUSDT'
vol = float(volatilites(symbol, start_time, end_time))
z_vente = z_achat + (1.63 * (vol / 2))
z_vente1 = z_achat - (1.5*(vol / 2))

while 1:
    i = i+1
    price = get_binance_price(symbol)
    prix.append(price)
    price = get_binance_price(symbol)
    prix.append(price)
    current_time = datetime.now().strftime('| %Y-%m-%d | %H:%M:%S |')


    btc_balance, usdt_balance = get_binance_account_balance()
    balance = (btc_balance * get_binance_price('BTCUSDT')) +  usdt_balance

    usdt_achat = (usdt_balance / price)-0.0001
    btc_vente = btc_balance -0.0001

    print("prix d'achat : ", round(z_achat,2),"prix de vente:", round(z_vente,2), "prix de vente:", round(z_vente1,2)," prix actuel: ", round(price,2), "Temps : ", current_time, round(vol,4), " | BTC : ", round(btc_balance,4), round(btc_vente,4), " | USDT : ", round(usdt_balance,4), round(usdt_achat,4), round(balance,4))

    if achat == 1:
        if price > z_vente:
            achat = 0
            z_achat = 0
            #vente_binance_order(symbol, 'SELL', btc_vente)

        if price < z_vente1 :
            achat = 0
            z_achat = 0
            #vente_binance_order(symbol, 'SELL', btc_vente)
    else:
        if prix[i] - prix[i-1] > 0 :
            achat = 1
            #create_binance_order(symbol , 'BUY', usdt_achat)
            z_achat = price
            z_vente = z_achat + (1.63 * (vol / 2))
            z_vente1 = z_achat - (1.5*(vol / 2))
