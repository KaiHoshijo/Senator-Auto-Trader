import trade_scrape as ts
import trade_db as db
import constants
import json
import csv

def write_pages_to_file(filename, max_pages):
    print(f'Max pages is {max_pages}')
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(constants.COLUMNS)
        for page_num in range(1, max_pages + 1):
            write_page(writer, page_num)

def write_page(writer, page_num):
    print(f'On page: {page_num}')
    page = ts.get_page(page_num)
    page = json.loads(page)
    for trade in page['data']:
        writer.writerow(ts.get_desired_info(trade))

def get_all_pages():
    max_pages = ts.get_page(1, 100)
    max_pages = json.loads(max_pages)
    write_pages_to_file(constants.TRADES_CSV, ts.get_total_pages(max_pages))

def create_db():
    cursor, connect = db.connect_db()
    db.create_table(cursor)
    db.convert_csv_to_db(cursor)
    db.close_db(connect)

if __name__ == '__main__':
    # get_all_pages()
    cursor, connect = db.connect_db()
    cols = ['COUNT(*)']
    cond = 'trade_type = ? AND trade_size > ?'
    vals = ('buy', '500')
    rows = db.get_rows(cursor, cols, cond, vals)
    for row in rows:
        print(row)
    db.close_db(connect)