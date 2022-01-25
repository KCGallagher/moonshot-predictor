# Import the data into a pandas csv

import pandas as pd

def import_csv(filename):
    """Imports the csv file at a given path
    
    :param filename: Path and name of file to import
    :type filename: str
    :return: Dataframe of csv file
    """
    return pd.read_csv(filename, sep=',')

def record_assays(df):
    """Removes SMILES data to create assay dataframe, where
    each row corresponds to a different assay (and a different 
    molecule)
    
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
    series =  df['SMILES']
    return series.to_frame()

def import_data(filename):
    """Imports the data at a given path
    
    :param filename: Path and name of file to import
    :type filename: str
    :return: Dataframes of assays and compounds
    :return type: pandas Dataframe
    """
    # Read in data
    df = import_csv(filename)

    df_assay = record_assays(df)
    df_compounds = record_compounds(df)
    
    return df_assay, df_compounds
