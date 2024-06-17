# Address for getting senator trades
TRADE_SITE = 'https://senate-stock-watcher-data.s3-us-west-2.amazonaws.com'
TRADE_DAILY = '/aggregate/all_daily_summaries.json'
TRADE_MAP = '/aggregate/filemap.xml'

# Columns for the rows to be saved to
COLUMNS = ['Politician', 'Party', 'Publication Date', 'Filing Date',
           'Trade Date', 'Filing Gap', 'Trade Type', 'Asset Type',
           'Asset Ticker', 'Trade Size']
# csv file name
TRADES_CSV = 'data/trades.csv'
# db file name
TRADES_DB = 'data/trades.db'
# API keys
ENDPOINT = 'https://paper-api.alpaca.markets'