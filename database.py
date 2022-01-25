# Creates a relational database from the binding data

import pandas as pd
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn


def main():
    input_data = "data/activity_data.csv"
    database = "sqlite/db/activity.db"

    # Read in data
    df = pd.read_csv(input_data)

    # Create a database connection
    conn = create_connection(database)

    # Read csv into database
    with conn:
        df.to_sql('activity', conn, if_exists='append', index=False)

    # Close connection if still open (fail-safe)
    conn.close

if __name__ == '__main__':
    main()
