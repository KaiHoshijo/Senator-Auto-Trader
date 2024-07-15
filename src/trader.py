import pandas_market_calendars as mcal
import constants
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.common.exceptions import APIError

trading_client = TradingClient(constants.KEY, constants.SECRET, paper = True)

def is_open(date):
    market = mcal.get_calendar('NYSE').schedule(start_date = date,
                                                end_date = date)
    return market.empty == False

def filter_symbol(symbol):
    symbol = symbol.replace(':US', '')
    return symbol

def get_position(symbol):
    try:
        # Get a specific position owned
        return trading_client.get_open_position(symbol)
    except APIError:
        return None

def is_asset_tradable(symbol):
    asset = trading_client.get_asset(symbol)
    return asset.tradable

def buy_stock(symbol, qty = 1):
    # Ensure that the symbol is written in the correct manner
    symbol = filter_symbol(symbol)
    if not is_asset_tradable(symbol):
        # raise Exception(f'{symbol} is not a tradable asset')
        return None
    market_order_data = MarketOrderRequest(
        symbol = symbol,
        qty = qty,
        side = OrderSide.BUY,
        time_in_force = TimeInForce.DAY
    )
    market_order = trading_client.submit_order(
        order_data = market_order_data
    )
    return market_order

def sell_stock(symbol, qty = 1):
    # Ensure that the symbol is written in the correct manner
    symbol = filter_symbol(symbol)
    if not is_asset_tradable(symbol):
        # raise Exception(f'{symbol} is not a tradable asset')
        return None
    if get_position(symbol) is None:
        # raise Exception(f'{symbol} is not owned')
        return None
    market_order_data = MarketOrderRequest(
        symbol = symbol,
        qty = qty,
        side = OrderSide.SELL,
        time_in_force = TimeInForce.GTC
    )
    market_order = trading_client.submit_order(
        order_data = market_order_data
    )
    return market_order
