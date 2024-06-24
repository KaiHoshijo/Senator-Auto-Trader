import constants
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def openSenate():
    # Creating driver to go to the Senate's financial reports
    driver = webdriver.Firefox()
    driver.get(constants.SENATE)
    # Returning the driver to be used to get the financial data
    return driver

def enterNameForSenate(driver, first, last):
    # Find the element for the first name

    # Enter the supplied first name

    # Find the element for the last name

    # Enter the supplied last name
    pass

def enterFillerTypeForSenate(driver, senator, senator_state = '',
                             candidate, candidate_state = '', former_senator):
    # Find the element for senator checkbox

    # Click senator checkbox if senator is true

    # Find the element for senator state

    # Select state based on supplied senator_state

    # Find the element for candidate checkbox

    # Click candidate checkbox if candidate is true

    # Find the element for candidate state

    # Select state based on supplied candidate_state

    # Find the element for former senator checkbox

    # Click the former senator checkbox if former_senator is true
    pass

def enterReportTypesForSenate(driver, reportData):
    # Find checkbox for each type of report
    
    # For every true boolean in reportData, click the checkbox
    pass

def enterDatesForSenate(driver, fromDate, toDate):
    # Find from date textbox

    # Enter date supplied by the variable fromDate

    # Find the to date textbox

    # Enter data supplied by the variable toDate
    pass

def enterSearch(driver):
    # Find the search reports button

    # Click the search reports button
    pass