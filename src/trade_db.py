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
    # Delete all the tables created
    drop_table = 'DROP TABLE IF EXISTS politicians;'
    cursor.execute(drop_table)
    drop_table = 'DROP TABLE IF EXISTS buy;'
    cursor.execute(drop_table)
    drop_table = 'DROP TABLE IF EXISTS sell;'
    cursor.execute(drop_table)
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

def create_politicians(cursor):
    # Creating the table to store all the politicians and their ids
    politic_table = \
    '''
        CREATE TABLE politicians(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            party TEXT NOT NULL
        );
    '''
    # Creating the politician table
    cursor.execute(politic_table)

def insert_politicians(cursor):
    # Taking from the trades table and putting in the politicians table
    politic_insert = \
    '''
        INSERT INTO politicians(
            name,
            party
        )
        SELECT DISTINCT politician, party FROM trades;
    '''
    # Executing the above command
    cursor.execute(politic_insert)

def create_buy(cursor):
    # Creating the table to store all the buy trades
    buy_table = \
    '''
        CREATE TABLE buy(
            politician_id INTEGER NOT NULL,
            trade_id INTEGER,
            publication_date TEXT NOT NULL,
            filing_date TEXT NOT NULL,
            trade_date  TEXT NOT NULL,
            filing_gap TEXT NOT NULL,
            asset_ticker TEXT DEFAULT NULL,
            trade_size INTEGER DEFAULT NULL,
            FOREIGN KEY (trade_id) REFERENCES trades(id)
        )
    '''
    # Executing the above command
    cursor.execute(buy_table)

def insert_buy(cursor):
    # Insert all the buy trades from the trades db and only get stocks
    insert_buy = \
    '''
        INSERT INTO buy(
            politician_id,
            trade_id,
            publication_date,
            filing_date,
            trade_date,
            filing_gap,
            asset_ticker,
            trade_size
        )
        SELECT politic.id, trades.id, publication_date, filing_date,
                trade_date, filing_gap, asset_ticker, trade_size
                FROM trades
            JOIN politicians AS politic ON politic.name = politician 
            WHERE trade_type = 'buy' AND asset_type = 'stock';
    '''
    # Executing the above command
    cursor.execute(insert_buy)

def create_sell(cursor):
    # Creating the table to store all the sell trades
    sell_table = \
    '''
        CREATE TABLE sell(
            politician_id INTEGER NOT NULL,
            trade_id INTEGER,
            publication_date TEXT NOT NULL,
            filing_date TEXT NOT NULL,
            trade_date TEXT NOT NULL,
            filing_gap TEXT NOT NULL,
            asset_ticker TEXT DEFAULT NULL,
            trade_size INTEGER DEFAULT NULL,
            FOREIGN KEY(trade_id) REFERENCES trades(id)
        )
    '''
    # Executing the above command
    cursor.execute(sell_table)

def insert_sell(cursor):
    # Insert all the sell trades from the trades db
    insert_sell = \
    '''
        INSERT INTO sell(
            politician_id,
            trade_id,
            publication_date,
            filing_date,
            trade_date,
            filing_gap,
            asset_ticker,
            trade_size
        )
        SELECT politic.id, trades.id, publication_date, filing_date,
                trade_date, filing_gap, asset_ticker,
                trade_size FROM trades
            JOIN politicians AS politic ON politic.name = politician
            WHERE trade_type = 'sell' AND asset_type = 'stock';
    '''
    # Executing the above command
    cursor.execute(insert_sell)

def convert_csv_to_db(cursor):
    with open(constants.TRADES_CSV, 'r') as f:
        reader = csv.reader(f)
        insert_db(cursor, reader)

def close_db(connect):
    # Finalize changes and close the connection
    connect.commit()
    connect.close()

def get_rows(cursor, db = 'trades', cols = ['*'], cond = None, vals = None):
    # Select only the columns passed through
    cols = ', '.join(cols)
    # Get the rows specified by the conditions
    query = f'SELECT {cols} FROM {db}'
    # Add the where-condition if one is specified
    if cond is not None:
        query += f' {cond}'
    # Account for the values added for the conditions
    if vals is not None:
        cursor.execute(query, vals)
    else:
        cursor.execute(query)
    return cursor.fetchall()

def delete_rows(cursor, db = 'trades', cond = None, vals = None):
    # Delete rows from trade without conditions
    query = f'DELETE FROM {db}'
    # Add the condition for the where
    if cond is not None:
        query += f' WHERE {cond}'
    # Execute with provided values
    if vals is not None:
        cursor.execute(query, vals)
    else:
        cursor.execute(query)