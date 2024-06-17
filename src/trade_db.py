import constants
import sqlite3

def connect_db():
    # Setting up trade database
    connect = sqlite3.connect(constants.TRADES_DB)
    cursor = connect.cursor()
    return cursor, connect