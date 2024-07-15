import trade_scrape as ts
import trader
import datetime
import time

def get_stocks():
    stocks = {'buy': [], 'sell': []}
    stocks['info'] = []
    # Get the current date
    current_day = datetime.datetime.today()
    if trader.is_open(current_day):
        print('Made it here')
        # Open the financial disclosures from the senate
        driver = ts.open_senate()
        driver.refresh()
        time.sleep(15)
        entries = ts.get_table(driver)
        today_stocks = ts.get_today(driver, entries)
        driver.close()
        for stock in today_stocks:
            ticker = stock[1]
            action = stock[2]
            stocks['info'].append([ticker, action])
            if action == 'BUY':
                res = trader.buy_stock(ticker)
                if res is not None:
                    print(f'Bought 1 of {ticker}')
                    stocks['buy'].append(ticker)
            elif action == 'SELL':
                res = trader.sell_stock(ticker)
                if res is not None:
                    print(f'Sold 1 of {ticker}')
                    stocks['sell'].append(ticker)
    return stocks

if __name__ == '__main__':
    stocks = get_stocks()
    with open('stock_data.txt', 'a') as stock_data:
        stock_data.write(f'Date: {str(datetime.datetime.today())}\n')
        stock_data.write(f'Total stocks: {stocks["info"]}\n')
        for stock in stocks['buy']:
            stock_data.write(f'\tBought: {str(stock)}\n')
        for stock in stocks['sell']:
            stock_data.write(f'\tSold: {str(stock)}\n')
