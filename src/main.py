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

def update_db(cursor, connect):
    # cursor, connect = db.connect_db()
    max_pages = ts.get_page(1, 100)
    max_pages = json.loads(max_pages)
    # Get the length of the new rows
    total_records = max_pages['meta']['paging']['totalItems']
    new_rows = total_records - len(db.get_all_rows(cursor))
    current_page = 1
    # Only update if there is at least one new trade
    print(f'Need to update {new_rows}')
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
    print(f'Capitol records vs our records: {post}')
    # db.close_db(connect)

if __name__ == '__main__':
    cursor, connect = db.connect_db()
    cols = ['*']
    cond = 'publication_date > ?'
    current_date = datetime.datetime.now() \
                    - datetime.timedelta(50)
    current_date = current_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    vals = (current_date,)
    db.delete_rows(cursor, cond, vals)
    update_db(cursor, connect)
    db.close_db(connect)