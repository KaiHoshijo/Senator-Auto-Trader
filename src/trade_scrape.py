import constants
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import selenium

def open_senate():
    # Creating driver to go to the Senate's financial reports
    driver = webdriver.Firefox()
    driver.get(constants.TRADES)
    # Returning the driver to be used to get the financial data
    return driver

def get_table(driver):
    try:
        # Get the table from capitoltrades
        table = driver.find_element(By.XPATH,
                                    '//table[@class=\"q-table trades-table\"]')
        # Get each element from the table
        entries = table.find_elements(By.XPATH, '//tr[@class=\"q-tr\"]')
        return entries
    except NoSuchElementException:
        raise Exception('Table is not found in capitol trades')

def get_today(entries, ignoreGreater = 15):
    today_trades = [] # Get only stocks published less than ignoreGreater
    # Iterate through the table and return only those that were published today
    for entry in entries[1:]:
        row = entry.text.split() # Get all text for that row
        # Ignore row if entry wasn't a stock or published today
        if 'Today' not in row or 'N/A' in row[:8]:
            continue
        name = row[0] + ' ' + row[1]
        today_index = row.index('Today')
        pub_date = row[today_index + 5]
        action = row[today_index + 7]
        if int(pub_date) > ignoreGreater:
            continue
        asset_ticker = row[today_index - 2]
        today_trades.append([name, asset_ticker, action])
    return today_trades 

