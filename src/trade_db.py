import constants
import sqlite3
import csv

def connect_db():
    # Setting up trade database
    connect = sqlite3.connect(constants.TRADES_DB)
    cursor = connect.cursor()
    return cursor, connect

def create_table(cursor):
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
    asset_ticker TEXT NOT NULL,
    trade_size INTEGER NOT NULL
    );
    '''
    # Executing the command to create the table
    cursor.execute(create_table)

def drop_table(cursor):
    # Command to delete the entire table
    drop_table = 'DROP TABLE trades;'
    cursor.execute(drop_table)

def convert_csv_to_db(cursor):
    with open(constants.TRADES_CSV, 'r') as f:
        reader = csv.reader(f)
        # Insert each value of the csv into the database
        insert_table = \
        '''
        INSERT INTO trades(
        politician, party, publication_date, filing_date, trade_date,
        filing_gap, trade_type, asset_type, asset_ticker, trade_size
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        '''
        cursor.executemany(insert_table, reader)

def get_all_rows(cursor):
    # Get all the records within trades
    rows = 'SELECT * FROM trades;'
    return cursor.execute(rows).fetchall()

def get_rows(cursor, cols, cond = None, vals = None):
    # Select only the columns passed through
    cols = ', '.join(cols)
    # Get the rows specified by the conditions
    query = f'SELECT {cols} FROM trades'

    # Add the condition to the where
    if cond is not None:
        query += f' WHERE {cond}'
        print(query)

    # Account for the values added for the conditions
    if vals is not None:
        cursor.execute(query, vals)
    else:
        cursor.execute(query)

    return cursor.fetchall()

def close_db(connect):
    # Finalize changes and close the connection
    connect.commit()
    connect.close()