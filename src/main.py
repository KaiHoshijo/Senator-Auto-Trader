import trade_scrape as ts
import trader
import datetime
from multiprocessing import Process

def get_stocks():
    # Get the current date
    current_day = datetime.datetime.today()
    if trader.is_open(current_day):
        # Open the financial disclosures from the senate
        driver = ts.open_senate()
        entries = ts.get_table(driver)
        today_stocks = ts.get_today(entries)
        driver.close()
        for stock in today_stocks:
            ticker = stock[1]
            action = stock[2]
            if action == 'BUY':
                trader.buy_stock(ticker)
            elif action == 'SELL':
                trader.sell_stock(ticker)

if __name__ == '__main__':
    get_stocks()