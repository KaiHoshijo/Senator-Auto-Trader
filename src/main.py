import trade_scrape as ts
import trader
import datetime

if __name__ == '__main__':
    # Get the current date
    current_day = datetime.datetime.today()
    # Only trade if the market is open
    if trader.is_open(current_day):
        # Get the transactions for today
        pass