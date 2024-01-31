import requests
import constants

def get_all_pages():
    for num in range(1, 101):
        yield get_page(num)

def get_page(num=1):
    # Capitol trades separates page by page for past senator trades
    # ?page= is what signifies what page, the website is on
    site = constants.TRADE_SITE + f"?page={num}&pageSize=100"
    response = requests.get(site)
    content = response.content
    return content