import constants
import requests
import trader


def get_trades_daily(day):
    # Get all daily summaries from api
    site = constants.TRADE_SITE + constants.TRADE_DAILY
    response = requests.get(site)
    # Returns the trades for the current day
