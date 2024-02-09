import trade_scrape as ts
import trade_db as db
import constants
import datetime
import json
import csv

def write_pages_to_file(filename, max_pages):
    # Given max pages, iterate through each page and add them to the file
    # specified in the constants module
    print(f'Max pages is {max_pages}')
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        for page_num in range(1, max_pages + 1):
            write_page(writer, page_num)

def write_page(writer, page_num):
    # Iterate through each trade in this page and write it to the file
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

def reset_db():
    # This is supposed to be used if something in the db goes wrong
    get_all_pages()
    create_db()

def update_db():
    cursor, connect = db.connect_db()
    max_pages = ts.get_page(1, 100)
    max_pages = json.loads(max_pages)
    # Get the length of the new rows
    total_records = max_pages['meta']['paging']['totalItems']
    total_rows = db.get_rows(cursor, ['id'], 'ORDER BY id DESC')[0][0]
    new_rows = total_records - total_rows
    current_page = 1
    # Only update if there is at least one new trade
    print(f'Total records: {total_records}')
    print(f'Total rows: {total_rows}')
    print(f'Need to update: {new_rows}')
    # If the db is out of sync, reset it
    if new_rows < 0:
        reset_db()
    while new_rows > 0:
        # Get all the rows available on the current page
        rows = ts.get_page(current_page, min(new_rows, 100))
        rows = json.loads(rows)
        rows = tuple([ts.get_desired_info(trade) for trade in rows['data']])
        db.insert_db(cursor, rows)
        # Max number of trades available is 100
        new_rows -= 100
        current_page += 1
    post = total_records - len(db.get_all_rows(cursor))
    print(f'Records: {post}')
    db.close_db(connect)

def get_party_between_dates(cursor, party, start, end=datetime.datetime.now()):
    cond = 'WHERE party = ? AND publication_date > ? AND publication_date < ? \
            AND asset_type = ?'
    vals = (party, start, end, 'stock')
    rows = db.get_rows(cursor, cond = cond, vals = vals)
    for row in rows:
        sold = db.get_sold_stock(cursor, row)
        if row[7] == 'buy' and len(sold) > 0:
            print(row)
            print(sold)

if __name__ == '__main__':
    # Getting the updated records
    update_db()
    # Connecting to the db
    cursor, connect = db.connect_db()

    # Setting the date for the last two months
    month = datetime.datetime.now() - datetime.timedelta(days = 120)
    month = datetime.datetime.strftime(month, '%Y-%m-%dT%H:%M:%SZ')

    get_party_between_dates(cursor, 'republican', month)

    # Closing db after getting data
    db.close_db(connect)