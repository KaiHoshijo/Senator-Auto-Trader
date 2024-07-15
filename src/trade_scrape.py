import constants
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.chrome.service import Service
import selenium
from pyvirtualdisplay import Display
import time

def open_senate():
    # Creating driver to go to the Senate's financial reports
    display = Display(visible = 0, size = (1600, 1200))
    display.start()
    service = Service(executable_path = '/usr/bin/chromedriver')
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service = service, options = options)
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

def get_next_table(driver):
    try:
        # Select the next tab
        # Prevent any stale elements
        driver.refresh()
        time.sleep(15)
        # Find the link itself
        next_button = driver.find_element(By.XPATH, '//a[@aria-label=\"Go to next page\"]')
        # Use that to get the parent element button
        next_button = next_button.find_element(By.XPATH, '//span/parent::*')
        next_button.click()
    except NoSuchElementException:
        raise Exception('Button is not found')

def get_today(driver, entries, ignoreGreater = 25):
    try:
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
        if 'Today' in entries[-1].text.split():
            get_next_table(driver)
            return today_trades + get_today(driver,
                    get_table(driver), ignoreGreater)
        return today_trades 
    except StaleElementReferenceException:
        driver.refresh()
        get_today(driver, get_table(driver))
