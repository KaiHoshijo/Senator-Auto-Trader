import trade_scrape as ts
import constants
import csv
import json

def write_pages_to_file(filename, max_pages):
    print(f'Max pages is {max_pages}')
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(constants.COLUMNS)
        for page_num in range(1, max_pages + 1):
            print(f'On page: {page_num}')
            page = ts.get_page(page_num)
            page = json.loads(page)
            for trade in page['data']:
                writer.writerow(ts.get_desired_info(trade))

def get_all_pages():
    max_pages = ts.get_page(1, 100)
    max_pages = json.loads(max_pages)
    write_pages_to_file('data/trades.csv', ts.get_total_pages(max_pages))

if __name__ == '__main__':
    get_all_pages()