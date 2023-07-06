
import sqlite3
from config import database

connection = None
try:
    # Connect to the database and create tables
    connection = sqlite3.connect(database)
    cursor = connection.cursor()

    # Create the userAccounts table
    cursor.execute('CREATE TABLE IF NOT EXISTS userAccounts (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')

    # Create the Credentials table
    cursor.execute('CREATE TABLE IF NOT EXISTS Credentials (id INTEGER PRIMARY KEY, website_id INTEGER, username TEXT, password TEXT, FOREIGN KEY(website_id) REFERENCES userAccounts(id))')

    # Commit the changes
    connection.commit()

except sqlite3.Error as db_error:
    # Handle errors related to database connection or other general database errors
    print("Error connecting to the database:", db_error.args[0])

finally:
    # Perform necessary cleanup or close the connection
    if connection:
        connection.close()
