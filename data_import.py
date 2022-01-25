# Import the data into a pandas csv

import pandas as pd

def import_csv(filename):
    """Imports the csv file at a given path
    
    :param filename: Path and name of file to import
    :type filename: string
    :return: Dataframe of csv file
    """
    return pd.read_csv(filename, sep=',')


def main():
    input_data = "data/activity_data.csv"

    # Read in data
    df = import_csv(input_data)
    print(df.head())


if __name__ == '__main__':
    main()