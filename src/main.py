import trade_scrape as ts
import trade_db as db
import constants
import matplotlib.pyplot as plt
import numpy as np
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
    print("Created trades")
    db.create_table(cursor)
    db.convert_csv_to_db(cursor)
    print("Created politicians")
    db.create_politicians(cursor)
    db.insert_politicians(cursor)
    print("Created buy")
    db.create_buy(cursor)
    db.insert_buy(cursor)
    print("Created sell")
    db.create_sell(cursor)
    db.insert_sell(cursor)
    # print("Created margin")
    # db.create_margin(cursor)
    # db.insert_margin(cursor)
    db.close_db(connect)

def reset_db():
    # This is supposed to be used if something in the db goes wrong
    get_all_pages()
    create_db()

def update_db():
    cursor, connect = db.connect_db()
    # Get the most recent date from the 'trades' db
    cols = ['MAX(publication_date), politician, filing_gap']
    db_trade = db.get_rows(cursor, 'trades', cols)[0]
    date, politician, gap = db_trade
    print(date, politician, gap)
    # Get the most recent trade from capitol trades
    page_num = 1
    page = ts.get_page(page_num, 1)
    page = json.loads(page)
    ct_trade = page['data'][0]
    ct_content = ts.get_desired_info(ct_trade)
    ct_date = ct_content[2]
    ct_politician = ct_content[0]
    ct_gap = ct_content[5]
    print(ct_date, ct_politician, ct_gap)
    # Update the db until the most recent published trade is in the db
    while date != ct_date and politician != ct_politician and gap != ct_gap:
        db.insert_db(cursor, [ct_content])
        page_num += 1
        page = ts.get_page(page_num, 1)
        page = json.loads(page)
        ct_trade = page['data'][0]
        ct_content = ts.get_desired_info(ct_trade)
        ct_date = ct_content[2]
        ct_politician = ct_content[0]
        ct_gap = ct_content[5]
        print(ct_date, ct_politician, ct_gap)
    cols = ['MAX(publication_date), politician, filing_gap']
    db_trade = db.get_rows(cursor, 'trades', cols)[0]
    date, politician, gap = db_trade
    print(date, politician, gap)
    db.drop_dependent(cursor)
    db.create_politicians(cursor)
    db.insert_politicians(cursor)
    print("Created buy")
    db.create_buy(cursor)
    db.insert_buy(cursor)
    print("Created sell")
    db.create_sell(cursor)
    db.insert_sell(cursor)
    # print("Created margin")
    # db.create_margin(cursor)
    # db.insert_margin(cursor)
    db.close_db(connect)

if __name__ == '__main__':
    # Getting the updated records
    reset_db()
    update_db()
    # Connecting to the db
    cursor, connect = db.connect_db()
    begin = "2023-01-01T00:00:00Z"
    end   = "2024-01-01T00:00:00Z"


    # Determining the portfolio average return through calculating the weight of 
    # each trade (trade buy price / total prices * 100) then multiplying the 
    # return % and taking the total sum of the results
    # query = \
    # f'''
    # WITH yearly_trades AS (
        # SELECT buy_publication_date AS date,
            #    sell_publication_date AS sdate,
            #    margin.asset_ticker as name,
            #    b.price AS price, s.price AS sprice,
            #    politicians.name as pname, percent_margin
            # FROM margin
            # JOIN buy AS b ON b.trade_id = margin.buy_trade_id
            # JOIN sell as s ON s.trade_id = margin.sell_trade_id
            # JOIN politicians ON b.politician_id = politicians.id
            # WHERE buy_publication_date BETWEEN \'{begin}\' AND \'{end}\' AND
                #   sell_publication_date BETWEEN \'{begin}\' AND \'{end}\'
    # ), return_calc AS (
        # SELECT date, sdate, name, pname, price, percent_margin, SUM(price * percent_margin) as day_total
        # FROM yearly_trades
        # GROUP BY date, sdate, name, pname, percent_margin
    # ), daily_return AS (
        # SELECT name, date,
            # (day_total / (SELECT SUM(day_total) FROM return_calc)) * 100 AS daily_return
        # FROM return_calc
    # )
    # SELECT name, AVG(daily_return) AS overall_return, date
    # FROM daily_return
    # GROUP BY name
    # ;
    # '''
    # cursor.execute(query)
    # rows = cursor.fetchall()
    # print(sum([row[1] for row in rows]))
    # for row in rows[:10]:
        # print(row)

    # Closing db after getting data
    db.close_db(connect)