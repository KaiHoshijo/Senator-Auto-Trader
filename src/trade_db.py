import constants
import sqlite3
import csv

def connect_db():
    # Setting up trade database
    connect = sqlite3.connect(constants.TRADES_DB)
    cursor = connect.cursor()
    return cursor, connect

def create_table(cursor):
    # Delete table if it already exists
    drop_table(cursor)
    # Command to create the table
    create_table = \
    '''
    CREATE TABLE trades(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        politician TEXT NOT NULL,
        party TEXT NOT NULL,
        publication_date TEXT NOT NULL,
        filing_date TEXT NOT NULL,
        trade_date  TEXT NOT NULL,
        filing_gap TEXT NOT NULL,
        trade_type TEXT NOT NULL,
        asset_type TEXT NOT NULL,
        asset_ticker TEXT DEFAULT NULL,
        trade_size INTEGER DEFAULT NULL
    );
    '''
    # Executing the command to create the table
    cursor.execute(create_table)

def drop_table(cursor):
    # Command to delete the entire table
    drop_table = 'DROP TABLE IF EXISTS trades;'
    cursor.execute(drop_table)

def insert_db(cursor, rows):
    # Insert each value of the csv into the database
    insert_table = \
    '''
    INSERT INTO trades(
    politician, party, publication_date, filing_date, trade_date,
    filing_gap, trade_type, asset_type, asset_ticker, trade_size
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    '''
    cursor.executemany(insert_table, rows)

def convert_csv_to_db(cursor):
    with open(constants.TRADES_CSV, 'r') as f:
        reader = csv.reader(f)
        insert_db(cursor, reader)

def get_all_rows(cursor):
    # Get all the records within trades
    rows = 'SELECT * FROM trades;'
    return cursor.execute(rows).fetchall()

def get_rows(cursor, cols = ['*'], cond = None, vals = None):
    # Select only the columns passed through
    cols = ', '.join(cols)
    # Get the rows specified by the conditions
    query = f'SELECT {cols} FROM trades'

    # Add the where-condition if one is specified
    if cond is not None:
        query += f' {cond}'

    # Account for the values added for the conditions
    if vals is not None:
        cursor.execute(query, vals)
    else:
        cursor.execute(query)

    return cursor.fetchall()

def delete_rows(cursor, cond = None, vals = None):
    # Delete rows from trade without conditions
    query = 'DELETE FROM trades'

    # Add the condition for the where
    if cond is not None:
        query += f' WHERE {cond}'

    # Execute with provided values
    if vals is not None:
        cursor.execute(query, vals)
    else:
        cursor.execute(query)

def close_db(connect):
    # Finalize changes and close the connection
    connect.commit()
    connect.close()

def get_trade_type_stocks(cursor, trade, trade_type, end_date = None):
    # Given a politician and a stock, find all recurring purchases were made
    id = trade[0]
    name = trade[1]
    pub_date = trade[3]
    trade_type = trade_type
    asset_ticker = trade[9]

    # Setting the filter conditions based off the provided trade
    cond = 'WHERE politician = ? AND publication_date > ? AND trade_type = ? \
            AND asset_ticker = ? AND id <> ?'
    vals = [name, pub_date, trade_type, asset_ticker, id]

    # Setting the end date if one exists
    if end_date is not None:
        cond += ' AND publication_date <= ?'
        vals.append(end_date)

    return get_rows(cursor, cond = cond, vals = tuple(vals))

def get_sold_stock(cursor, trade):
    # Given when a stock is bought, find when the stock is sold
    name = trade[1]
    pub_date = trade[3]
    trade_type = 'sell'
    asset_ticker = trade[9]

    cond = 'WHERE politician = ? AND publication_date > ? AND trade_type = ? \
            AND asset_ticker = ?'
    vals = (name, pub_date, trade_type, asset_ticker)
    return get_rows(cursor, cond = cond, vals = vals)