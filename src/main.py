import trade_scrape as ts
import csv
import json

def write_pages_to_file(filename):
    with open(filename, "a") as f:
        writer = csv.writer(f)


if __name__ == "__main__":
    val = ts.get_page(3, 10)
    val = json.loads(val)
    for i in val['data']:
        print(ts.get_desired_info(i))