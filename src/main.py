import trade_scrape as ts
import csv
import json

def write_pages_to_file(filename):
    with open(filename, "a") as f:
        writer = csv.writer(f)


if __name__ == "__main__":
    val = ts.get_page(1, 0)
    val = json.loads(val)
    print(val['data'][0])
    print(val['data'][0].keys())