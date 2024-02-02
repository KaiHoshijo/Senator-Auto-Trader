import trade_scrape as ts
import constants
import csv
import json

def write_pages_to_file(filename, max_pages):
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(constants.COLUMNS)
        for page_num in range(1, max_pages + 1):
            page = ts.get_page(page_num)
            page = json.loads(page)
            for trade in page['data']:
                writer.writerow(ts.get_desired_info(trade))

if __name__ == '__main__':
    max_pages = ts.get_page(1, 10)
    max_pages = json.loads(max_pages)
    # write_pages_to_file('data/trades.csv', ts.get_total_pages(max_pages))
    # write_pages_to_file('data/trades.csv', 2)
    for trade in max_pages['data']:
        print(ts.get_desired_info(trade))
