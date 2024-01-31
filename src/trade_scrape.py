import requests
import constants
from bs4 import BeautifulSoup as bs

def get_page(num=1):
    print(num)
    # Capitol trades separates page by page for past senator trades
    # ?page= is what signifies what page, the website is on
    site = constants.TRADE_SITE + f"?page={num}"
    print(site)
    response = requests.get(site)
    content = response.content
    # Prettifying the data through BeautifulSoup
    soup = bs(content, "html.parser")