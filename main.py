import requests
from bs4 import BeautifulSoup as bs

# Getting the senator trades from Capitol Trades 
response = requests.get("https://www.capitoltrades.com/trades")
content = response.content

# Prettifying the data through BeautifulSoup
soup = bs(content, 'html.parser')
print(soup.prettify())