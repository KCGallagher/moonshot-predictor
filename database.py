# Creates a relational database from the binding data

import pandas as pd  # noqa
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

def delete_molecule(conn, id):
    """
    Delete a molecule by molecule id
    :param conn:  Connection to the SQLite database
    :param id: id of the molecule
    :return:
    """
    sql = 'DELETE FROM assays WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()

def remove_attribute(conn, attr):
    """
    Remove an attribute of all molecules
    :param conn:  Connection to the SQLite database
    :param attr: molecule attribute
    :return:
    """
    sql = 'UPDATE assays SET SMILES = NULL'
    cur = conn.cursor()
    cur.execute(sql) 
    conn.commit()

def main():
    input_data = "data/activity_data.csv"
    database = "sqlite/db/activity.db"

    # Read in data
    df = pd.read_csv(input_data)

    # Create a database connection
    conn = create_connection(database)

   
    with conn:
        # Read csv into database
        df.to_sql('assays', conn, if_exists='replace', index=False)

        # Delete task in database
        remove_attribute(conn, "SMILES")
        
        # Test output from database
        df2 = pd.read_sql_query("SELECT * from assays", conn)
        print(df2.head())

    # Close connection if still open (fail-safe)
    conn.close

if __name__ == '__main__':
    main()
