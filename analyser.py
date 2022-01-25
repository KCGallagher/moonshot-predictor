# Provides analysis on compound and assay data

import pandas

def analyse_compounds(df_assay, df_compounds, name, func, **kwargs):
    """Analyse compound/assay data and add compound attributes to dataframe
    
    :param df: Dataframe of input data
    :type df: Pandas Dataframe
    :param func: Method to evaluate compound property
    :type func: First-order function, should return column of values
    :param name: Name of new property
    :type name: str
    :return: Dataframe of assay data
    """
    df_compounds[name] = func(df_assay, **kwargs)
    return df_compounds



def count_data_points(df, count_unique = False):
    """Print number of non-null values in each column
    
    :param df: Dataframe of input data
    :type df: Pandas Dataframe
    :param count_unique: Whether to only count unique elements
    :type count_unique: Bool
    """
    for header in df.columns.values:
        count = df[header].nunique() if count_unique else df[header].count()
        print(f"{header}: {count} values")
