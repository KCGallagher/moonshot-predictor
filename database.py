# Creates a relational database from the binding data

# Methods here do not use full input sanitisation and 
# may be vulnerable to SQL injection attacks, however
# this script is designed for internal use only.

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

def print_head(conn, table):
    sql = "SELECT * from {}".format(table)  # Not secure - see header
    df = pd.read_sql_query(sql, conn)
    print(df.head())

def connect_tables(conn, table_1, key_1, table_2):
    # Add primary key in table_1 as foreign key in table 2
    reference = (table_1 + "(" + key_1 + ")")
    sql = ('ALTER TABLE {} ADD FOREIGN KEY {} REFERENCES {}'
           .format(table_2, key_1, reference))
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    return table_1


def connect_tables(conn, table_1, key_1, table_2):
    # Add primary key in table_1 as foreign key in table 2
    # Sadly sqlite is limited so I must create a new table:

    # Rename table

    # Create new table with foreign key

    # Copy data into new table
    
    reference = (table_1 + "(" + key_1 + ")")
    sql = ('ALTER TABLE {} ADD FOREIGN KEY {} REFERENCES {}'
           .format(table_2, key_1, reference))
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    return table_1


def main():
    input_data = "data/activity_data.csv"
    database = "sqlite/db/activity.db"

    # Read in data
    df = pd.read_csv(input_data)

    # Create a database connection
    conn = create_connection(database)

   
    with conn:
        # Create assays table
        df.drop(['SMILES'], axis = 1).to_sql('assays', conn, if_exists='replace', index=False)

        # Create compounds table
        df['SMILES'].to_sql('compounds', conn, if_exists='replace', index=False)
        connect_tables(conn, 'compounds', 'SMILES', 'assays')
        
        # Test output from database
        print_head(conn, 'compounds')

    # Close connection if still open (fail-safe)
    conn.close

if __name__ == '__main__':
    main()
