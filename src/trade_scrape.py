import constants
import requests
import json

def get_all_pages(max_pages):
    for num in range(1, max_pages + 1):
        yield get_page(num)

def get_page(num=1,size=100):
    # Capitol trades separates page by page for past senator trades
    # ?page= is what signifies what page, the website is on
    site = constants.TRADE_SITE + f'?page={num}&pageSize={size}'
    response = requests.get(site)
    content = response.content
    return content

def get_total_pages(content):
    val = json.loads(content)
    return val['meta']['paging']['totalPages']

def get_desired_info(trade):
    name = trade['politician']['firstName'] + ' ' \
           + trade['politician']['lastName']
    party = trade['politician']['party']
    pubDate = trade['pubDate']
    filingDate = trade['filingDate']
    txDate = trade['txDate']
    reportingGap = trade['reportingGap']
    txType = trade['txType']
    assetType = trade['asset']['assetType']
    assetTicker = trade['asset']['assetTicker']
    assetTicker = assetTicker if assetTicker is not None else ''
    tradeSize = trade['size']
    tradeSize = tradeSize if tradeSize is not None else -1
    return [name, party, pubDate, filingDate, txDate, reportingGap, txType,
            assetType, assetTicker, tradeSize]