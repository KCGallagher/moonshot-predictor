# Import the data into a pandas csv

import pandas as pd

def import_csv(filename):
    """Imports the csv file at a given path
    
    :param filename: Path and name of file to import
    :type filename: string
    :return: Dataframe of csv file
    """
    return pd.read_csv(filename, sep=',')

def record_assays(df):
    """Removes SMILES data to create assay dataframe
    
    :param df: Dataframe of input data
    :type df: Pandas Dataframe
    :return: Dataframe of assay data
    """
    #Still need to sort this data
    return df.drop(['SMILES'], axis = 1)

def record_compounds(df):
    """Isolate SMILES data to create compound dataframe
    
    :param df: Dataframe of input data
    :type df: Pandas Dataframe
    :return: Dataframe of assay data
    """
    return df['SMILES']


def main():
    input_data = "data/activity_data.csv"

    # Read in data
    df = import_csv(input_data)

    df_assay = record_assays(df)
    df_compounds = record_compounds(df)
    
    print(df_assay.head())
    print(df_compounds.head())

    # Still need to implement foreign key

if __name__ == '__main__':
    main()