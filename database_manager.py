# Database Manager - from slite3 course docs.

import re
import csv
import sqlite3
from pathlib import Path


class DatabaseManager():
    def __init__(self, database_path: str):
        """
        Parameters
        ----------
        database_path: str
            Full path of existing SQLite database or one to be created automatically
        """

        # Store SQLite database path for reference
        self._database_path = database_path

        # Connect to and Create (if doesn't already exist) SQLite database
        self._conn = sqlite3.connect(database_path)

        # List of tables that need to be dropped to reset the SQLite database
        self._drop_order = ('compounds', 'submissions',)

    def get_conn(self):
        """
        get_conn returns a connection to the SQLite database self._database_path

        Returns
        -------
            SQLite connection object
        """
        return self._conn

    def drop_all(self):
        """
        drop_all drops all tables created by this class to reset the SQLite database
        """

        # Get connection to SQLite database
        conn = self.get_conn()

        # Drop all tables in dependency order
        for table_name in self._drop_order:
            conn.execute('DROP TABLE IF EXISTS ' + table_name)

    def create(self):
        """
        create - creates all tables required by this class in the SQLite database
        """

        # Get connection to SQLite database
        conn = self.get_conn()

        # Create a table to store all COVID Moonshot submissions
        conn.execute('''
            CREATE TABLE submissions
            (
                submission_id VARCHAR(20) PRIMARY KEY,
                name_code CHAR(3) not null,
                institute_code CHAR(3) not null,
                random_id CHAR(8) not null
            )
        ''')

        # Create a table to store all COVID Moonshot compound submissions
        conn.execute('''
            CREATE TABLE compounds
            (
                compound_id VARCHAR(20) PRIMARY KEY,
                smiles VARCHAR(2000) not null,
                submission_id VARCHAR(20) not null,
                made VARCHAR(5) not null,
                inchi_key CHAR(27) not null,
                MW DECIMAL not null,
                r_avg_IC50 DECIMAL,
                FOREIGN KEY(submission_id) REFERENCES submission_id(submission_id) 
            )
        ''')

    def show_tables(self):
        """
        show_tables - prints out the SQL used to built all the tables in our SQLite database
        """

        # Get a connection to our SQLite database
        conn = self.get_conn()

        # Generate a list of tables within our SQLite database

        # Execute an SQL statement to get a cursor object to iterate over the SQL statement results
        cur = conn.execute('''
            SELECT 
                name
            FROM 
                sqlite_master 
            WHERE 
                type ='table' AND 
                name NOT LIKE 'sqlite_%'
        ''')

        tables = []

        for row in cur.fetchall():
            tables.append(row[0])

        # Iterate over the tables in our SQLite database and fetch and print their SQL definitions
        for table in tables:
            cur = conn.execute('SELECT  sql  FROM  sqlite_master  WHERE name=\'' + table + '\'')

            row = cur.fetchone()

            if row is not None:
                print(table+'\n')

                print(row[0])
            else:
                print('Table ' + table + ' not found')

    def populate_submissions_table(self, all_data_file: Path):
        """
        Populates the table submissions by reading out 
        all of the unique submissions from $all_data_file
        """

        # Get database connection
        conn = self.get_conn()

        # Compile REGEX for submission ID
        sub_pattern = re.compile('(\w{3})-(\w{3})-(\w{8})-(\d+)')

        # Open the data file
        with open(all_data_file, 'r') as fh:
            # Initialise a CSV reader
            reader = csv.reader(fh, delimiter=',')

            # Create dictionary to generate unique list with
            unique_submissions = {}

            # Iterate rows in data file
            for cols in reader:
                # Get submission ID
                sub_id = cols[1]

                # Apply regular expression
                # Lots of ways of extracting what we need of course
                match = sub_pattern.match(sub_id)

                if match:
                    # Get submitter three letter code
                    name_code = match.group(1)
                    # Get institute three letter code
                    institute_code = match.group(2)
                    # Get random component of submission ID
                    random_id = match.group(3)

                    # Generate unique key, which is just $sub_id minus the final -INT
                    key = f'{name_code}-{institute_code}-{random_id}'

                    # The value we store here is the value we know we need for the SQL statement below
                    unique_submissions[key] = (key, name_code, institute_code, random_id)
                else:
                    # Warn if expected pattern doesn't match
                    print(f'Warning f{sub_id} doesn\'t conform to pattern')

            # Execute SQL statement to insert all unique submissions
            conn.executemany('INSERT INTO submissions (submission_id, name_code, institute_code, random_id) VALUES(?,?,?,?)', unique_submissions.values())

    def populate_compounds_table(self, all_data_file: Path):
        """
        Populate compounds table using $all_data_file
        """

        # Get database connection
        conn = self.get_conn()

        # Compile submission ID pattern
        sub_pattern = re.compile('(\w{3})-(\w{3})-(\w{8})-(\d+)')

        # Initialise compound list
        compounds = []

        # Open the data file
        with open(all_data_file, 'r') as fh:
            # Initialise a CSV reader
            reader = csv.DictReader(fh, delimiter=',')

            # Used to identify duplicate CIDS
            cmp_idx = {}

            # Iterate rows in data file
            for cols in reader:
                # Extract fields we require
                smiles = cols['SMILES']
                comp_id = cols['CID']
                made = cols['MADE']
                inchi_key = cols['InChIKey']
                mw = cols['MW']
                r_avg_IC50 = cols['r_avg_IC50']

                # Identify and skup duplicate CIDs
                if comp_id in cmp_idx:
                    print(f'Compound ID {comp_id} already uploaded')
                    continue

                # Remember that we have seen this CID
                cmp_idx[comp_id] = 1

                # Apply pattern to submission ID
                match = sub_pattern.match(comp_id)

                if match:
                    name_code = match.group(1)
                    institute_code = match.group(2)
                    random_id = match.group(3)

                    sub_id = f'{name_code}-{institute_code}-{random_id}'

                    # Store all the data we need to upload this compound
                    compounds.append((comp_id, sub_id, smiles, made, inchi_key, mw, r_avg_IC50))

            # Upload compounds
            conn.executemany('INSERT INTO compounds (compound_id, submission_id, smiles, made, inchi_key, mw, r_avg_IC50) VALUES(?,?,?,?,?,?,?)', compounds)

    def print_number_of_submission_institutes(self):
        """
        Print the number of institutes that have submitted compounds 
        to the COVID Moonshot project
        """

        # Get database connection
        conn = self.get_conn()

        # Run SQL count statement
        cur = conn.execute('''
            SELECT
                COUNT(distinct institute_code)
            FROM
                submissions
        ''')

        # Fetch results
        row = cur.fetchone()

        # Print results
        if row is not None:
            print(f'Number of submission institutes {row[0]}')

    def print_number_of_compounds_per_institute(self):
        """
        Print out the number of compound submissions per institute 
        with the institute with the most submissions first in the list
        """

        # Get a database connection
        conn = self.get_conn()

        # Execute complex SQL statement
        cur = conn.execute('''
            SELECT
                b.institute_code,
                COUNT(a.compound_id)
            FROM
                compounds a,
                submissions b
            WHERE
                a.submission_id = b.submission_id
            GROUP BY
                b.institute_code
            ORDER BY
                COUNT(a.compound_id) DESC
        ''')

        # Print out results
        for row in cur:
            print(f'{row[0]}/{row[1]}')

    def print_number_of_compounds_made(self):
        """
        Print out the number of compounds which have been made in the form
        "Made X of T compounds (X/T*100)"
        """

        # Get database connection
        conn = self.get_conn()

        # Execute SQL statement
        cur = conn.execute('''
            SELECT
                made,
                COUNT(compound_id)
            FROM
                compounds
            GROUP by
                made
            ORDER BY 
                made DESC
        ''')

        # Use Python loop to work out made and unmade totals
        made = 0
        unmade = 0

        for row in cur:
            if row[0] == 'TRUE':
                made = row[1]
            else:
                unmade = row[1]

        # Print out answer
        print(f'Made {made} of {made+unmade} compounds ({(made/(made+unmade))*100:.2f}%)')

    def print_number_of_unique_inchi_keys(self):
        """
        InChI Keys are one way of representing unique compounds.  Write some SQL
        to look for duplicate submissions and output the number of duplicate compounds
        """

        # Get database connection
        conn = self.get_conn()

        # Run SQL statement
        cur = conn.execute('''
            SELECT
                COUNT(distinct inchi_key)
            FROM
                compounds 
            
            UNION ALL 
            
            SELECT
                COUNT(compound_id)
            FROM
                compounds
        ''')

        # Get and print results
        unique_inchi_keys = cur.fetchone()[0]
        number_of_compounds = cur.fetchone()[0]

        print(f'Number of unique InChI Keys {unique_inchi_keys} for {number_of_compounds} compounds')

    def print_top_10_compounds(self):
        """
        Print out the top 10 compounds as ranked by their r_avg_IC50 values
        """

        # Get database connection
        conn = self.get_conn()

        # Execute SQL statement
        cur = conn.execute('''
            SELECT
                compound_id,
                r_avg_IC50,
                smiles
            FROM
                compounds
            WHERE
                r_avg_IC50 IS NOT NULL
            ORDER BY 
                r_avg_IC50 ASC 
            LIMIT 10
        ''')

        # Print out results
        for row in cur:
            print(f'Compound ID => {row[0]}, IC50 => {row[1]:.4f}uM, SMILES => {row[2]}')