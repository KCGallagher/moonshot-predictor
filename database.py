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
    """
    Print head of table (internal conversion to csv)
    :param conn:  Connection to the SQLite database
    :param table: Name of table within open database
    :return:
    """
    sql = "SELECT * from {}".format(table)  # Not secure - see header
    df = pd.read_sql_query(sql, conn)
    print(df.head())

def find_columns(conn, table):
    """
    Return columns of table (internal conversion to csv)
    :param conn:  Connection to the SQLite database
    :param table: Name of table within open database
    :return:
    """
    sql = "SELECT * from {}".format(table)  # Not secure - see header
    df = pd.read_sql_query(sql, conn)
    return df.columns.values

def connect_tables(conn, table_1, key_1, table_2):
    """
    Connect two tables within database - Adds the primary
    key in table_1 as foreign key in table 2. This requires
    creation of a new table in sqlite.

    :param conn:  Connection to the SQLite database
    :param table_1: Name of parent table
    :param key_1:   Name of column in table_1 to use as foreign key
    :param table_2: Name of child table
    :return:
    """
    cur = conn.cursor()  

    # Rename table
    cur.execute("DROP TABLE IF EXISTS _old_t") # for protection in case clean up not reached
    rename_sql = "ALTER TABLE {} RENAME TO {}".format(table_2, '_old_t')
    cur.execute(rename_sql)

    # Create new table with foreign key
    table_2_titles = ", ".join(find_columns(conn, '_old_t'))
    table_2_titles += ", {} VARCHAR".format(key_1)  # For foreign key column
    create_sql = ("CREATE TABLE {2} ({3}, CONSTRAINT FK_{0} FOREIGN KEY ({0}) REFERENCES {1} ({0}))"
        .format(key_1, table_1, table_2, table_2_titles))
    cur.execute(create_sql)

    # Add foreign key data to import table
    add_sql_a = "ALTER TABLE _old_t ADD {}".format(key_1)
    add_sql_b = "INSERT INTO _old_t ({0}) SELECT {0} FROM {1}".format(key_1, table_1)
    cur.execute(add_sql_a)
    cur.execute(add_sql_b)
    
    # Copy data into new table
    insert_sql = "INSERT INTO {} SELECT * FROM _old_t".format(table_2)
    cur.execute(insert_sql)

    # Delete temporary table
    cur.execute("DROP TABLE IF EXISTS _old_t")

    conn.commit()
    return table_2


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
        print_head(conn, 'assays')

    # Close connection if still open (fail-safe)
    conn.close

if __name__ == '__main__':
    main()
