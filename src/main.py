import trade_scrape as ts
import trader
import datetime

if __name__ == '__main__':
    # Get the current date
    current_day = datetime.datetime.today()
    # Only trade if the market is open
    if trader.is_open(current_day):
        # Open the financial disclosures from the senate
        driver = ts.openSenate()
        # Enter the permissions before searching
        ts.enterPermission(driver)
        # Enter a date to get reports from
        ts.enterDatesForSenate(driver, '06/15/2024', '')
        # Get the transactions for today
        ts.enterSearch(driver)
