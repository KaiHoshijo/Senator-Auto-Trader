import constants
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import selenium

def openSenate():
    # Creating driver to go to the Senate's financial reports
    driver = webdriver.Chrome()
    driver.get(constants.SENATE)
    # Returning the driver to be used to get the financial data
    return driver

def enterPermission(driver):
    try:
        # Find the permissions checkbox
        button = driver.find_element(By.XPATH, '//input[@type=\'checkbox\']')
        # Click the button and continue
        button.click()
    except NoSuchElementException:
        raise Exception('Permission button is not found')


def enterNameForSenate(driver, first, last):
    try:
        # Find the element for the first name
        first_elm = driver.find_element(By.XPATH,
                                '//input[@id=\'firstName\',@type=\'text\']')
        # Enter the supplied first name
        first_elm.send_keys(first)
        # Find the element for the last name
        last_elm = driver.find_element(By.XPATH,
                                '//input[@id=\'lasttName\',@type=\'text\']')
        # Enter the supplied last name
        last_elm.send_keys(last)
    except NoSuchElementException:
        raise Exception('First or Last name textbox is not found')

def enterFillerTypeForSenate(driver, senator, senator_state,
                             candidate, candidate_state, former_senator):
    try:
        # Find the element for senator checkbox
        senate_checkbox = driver.find_element(By.XPATH,
                        '//input[@class=\'form-check-input senator_filer\']')
        # Click senator checkbox if senator is true
        if senator:
            senate_checkbox.click()
            # Find the element for senator state
            senate_state = driver.find_element(By.XPATH,
                        '//select(@name=\'senator_state\')')
            # Select state based on supplied senator_state
            senate_state.send_keys(senator_state)
        # Find the element for candidate checkbox
        candidate_checkbox = driver.find_element(By.XPATH,
                        '//input[@class=\'form-check-input candidate_filer\']')
        # Click candidate checkbox if candidate is true
        if candidate:
            candidate_checkbox.click()
            # Find the element for candidate state
            candid_state = driver.find_element(By.XPATH,
                        '//select[@name=\'candidate_state\']')
            # Select state based on supplied candidate_state
            candid_state.send_keys(candidate_state)
        # Find the element for former senator checkbox
        former_checkbox = driver.find_element(By.XPATH,
                        '//input[@class=\'form-check-input\']')
        # Click the former senator checkbox if former_senator is true
        if former_senator:
            former_checkbox.click()
    except NoSuchElementException:
        raise Exception('A filler type was not found')

def enterReportTypesForSenate(driver, reportData):
    try:
        # Find checkbox for each type of report
        report_boxes = driver.find_elements(By.XPATH,
                            '//input[@id=\'reportTypes\']')
        # For every true boolean in reportData, click the checkbox
        for box, check in zip(report_boxes, reportData):
            if check:
                box.click()
    except NoSuchElementException:
        raise Exception('A report type was not found')

def enterDatesForSenate(driver, fromDate, toDate):
    try:
        # Find from date textbox
        from_date = driver.find_element(By.XPATH, '//input[@id=\'fromDate\']')
        # Enter date supplied by the variable fromDate
        from_date.send_keys(fromDate)
        # Find the to date textbox
        to_date = driver.find_element(By.XPATH, '//input[@id=\'toDate\']')
        # Enter data supplied by the variable toDate
        to_date.send_keys(toDate)
    except NoSuchElementException:
        raise Exception('From date or to date was not found')

def enterSearch(driver):
    try:
        # Find the search reports button
        button = driver.find_element(By.XPATH, '//button[@type=\'submit\']')
        # Click the search reports button
        button.click()
    except NoSuchElementException:
        raise Exception('Submit button is not found')