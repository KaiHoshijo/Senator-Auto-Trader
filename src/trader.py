import pandas_market_calendars as mcal
import vectorbt as vbt
import constants
import datetime
import alpaca_trade_api as tradeapi
import time

vbt.settings.data['alpaca']['key_id'] = constants.KEY
vbt.settings.data['alpaca']['secret_key'] = constants.SECRET
trader = tradeapi.REST(key_id = constants.KEY, secret_key = constants.SECRET,
                       base_url = constants.ENDPOINT)

def is_open(date):
    market = mcal.get_calendar('NYSE').schedule(start_date = date,
                                                end_date = date)
    return market.empty == False

def get_trade(symbol, date):
    date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
    if int(datetime.datetime.strftime(date, "%H")) > 15:
        date = date + datetime.timedelta(days = 1)
    # Check market at 9 AM
    date = datetime.datetime.strftime(date, '%Y-%m-%d') + ' 09:00:00'
    date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    while not is_open(date):
        date = date + datetime.timedelta(days = 1)
    other = date + datetime.timedelta(days = 1)
    # Given a date, find the price of the desired symbol
    try:
        data = vbt.AlpacaData.download(symbol, start = date, end = other,
                                    timeframe = '1m')
        return data.get("Close")[0]
    except Exception as e:
        print(f"Symbol {symbol} had error {e} on date {date}")
        return -1
    
def buy_stock(symbol, qty = 1, type = 'market', tif = 'gtc'):
    # Buy the stock at the quantity specified
    buy = trader.submit_order(
        symbol = symbol,
        side = 'buy',
        qty = 1,
        type = type,
        time_in_force = tif
    )
    print(f'Bought {qty} amount of {symbol}')
    # Get the id of the stock purchased
    buy_id = buy.id
    while True:
        time.sleep(1)
        if is_order_filled(symbol, buy_id):
            break

def sell_stock(symbol, qty = 1, type = 'market', tif = 'gtc'):
    # Sell the stock at the quantity specified
    sell = trader.submit_order(
        symbol = symbol,
        side = 'sell',
        qty = 1,
        type = type,
        time_in_force = tif
    )
    print(f'Sold {qty} amount of {symbol}')
    # Get the id of the stock sold
    sell_id = sell.id
    while True:
        time.sleep(1)
        if is_order_filled(symbol, sell_id):
            break

def is_order_filled(symbol, stock_id):
    # Wait until the stock has been purchased
    order = trader.get_order(stock_id)
    if order.status == 'filled':
        price = float(order.filled_avg_price)
        print(f'Symbol {symbol} has been bought at {price}')
        return True
    return False