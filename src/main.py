import trade_scrape as ts
import json

if __name__ == "__main__":
    val = ts.get_page(1)
    val = json.loads(val)
    print(val['data'][0])
    print(val['data'][0].keys())