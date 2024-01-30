import requests
import constants
from bs4 import BeautifulSoup as bs

def get_page(num=1):
    # Capitol trades separates page by page for past senator trades
    # ?page= is what signifies what page, the website is on
    response = requests.get(constants.TRADE_SITE + f"?page={num}")
    content = response.content
    # Prettifying the data through BeautifulSoup
    soup = bs(content, 'html.parser')
    return soup

    

def get_trade_rows(soup):
    # The data for the politician and the trade are located within the table
    # with class 'q-table trades-table'  
    # Within that table, the order of the columns is as follows:
    # politician, traded issuer, published, traded, filed after, owner, type,
    # size, and price
    politic_table = soup.find('table', attrs={'class': 'q-table trades-table'})
    # Within the tbody, each tr with class 'q-tr' will be a politician and a
    # trade
    politic_body = politic_table.find('tbody')
    politic_rows = politic_body.find_all('tr', attrs={'class': 'q-tr'})
    return politic_rows

def get_name(row):
    # This is the politiican name that purchased the stock
    return row.find('h3', attrs={'class':
                                 'q-fieldset politician-name'}).get_text()

def get_traded_issuer(row):
    # This is the traded issuer name as well as the ticker
    return [row.find('h3', attrs={'class':
                                  'q-fieldset issuer-name'}).get_text(),
            row.find('span', attrs={'class':
                                    'q-field issuer-ticker'}).get_text()]

def get_published(row):
    # This is when the trade was released to the public
    row_td = row.find('td', attrs={'class': 'q-td q-column--pubDate'})
    return [row_td.find('div', attrs={'class':
                                      'q-label'}).get_text(),
            row_td.find('div', attrs={'class':
                                       'q-value'}).get_text()]

def get_traded(row):
    # This is when the trade actually occured
    row_td = row.find('td', attrs={'class': 'q-td q-column--txDate'})
    return [row_td.find('div', attrs={'class':
                                      'q-label'}).get_text(),
            row_td.find('div', attrs={'class':
                                       'q-value'}).get_text()]

def get_trade_gap(row):
    # This is the time difference between publication and the trade
    row_td = row.find('td', attrs={'class': 'q-td q-column--reportingGap'})
    val = row_td.contents[0].contents
    return [val[1].get_text(), val[2].get_text()]

    # return [row_td.find('div', attrs={'class':
                                    #   'q-label'}).get_text(),
            # row_td.find('span', attrs={'class':
                                    #    'reporting-gap-tier--1'}).get_text()]

def get_owner(row):
    # This is the person who actually owns the stock
    row_td = row.find('td', attrs={'class': 'q-td q-column--owner'})
    return row_td.find('span', attrs={'class':
                                      'q-label'}).get_text()

def get_type(row):
    # This is whether the politiican bought or sold the stock
    row_td = row.find('td', attrs={'class': 'q-td q-column--txType'})
    return row_td.find('div').get_text().strip()

def get_size(row):
    # This is the size of which the politiican purchased the stock
    row_td = row.find('td', attrs={'class': 'q-td q-column--value'})
    return row_td.find('span', attrs={'class': 'q-label'}).get_text()

def get_price(row):
    # This is the price of the stock
    row_td = row.find('td', attrs={'class':
                                 'q-td q-column--price'}).contents
    return row_td[0].get_text().strip()