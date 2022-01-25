# Methods for analysing the data 

import numpy as np
import pandas as pd
class AnalysisMethods:
    """Collection of methods to generate information about target compounds
    """

    @staticmethod
    def type_of_amide(df):
        """Determines whether molecule is a acrlyamide or chloroacetamide
        
        :param df: Input dataframe of assay data
        :type df: pandas Dataframe
        :return: pandas Series
        """
        return (df['acrylamide'] | df['chloroacetamide'])

    @staticmethod
    def pIC50(df, metric = 'f_avg_IC50'):
        """Determines pIC50, using specified IC50 metric.
        
        :param df: Input dataframe of assay data
        :type df: pandas Dataframe
        :return: pandas Series
        """
        return pd.Series(-np.log10(df[metric]))

    @staticmethod
    def pIC50_threshold(df, metric = 'f_avg_IC50', threshold = 0):
        """Determines whether pIC50 is over a given threshold,
        using specified IC50 metric. Binary classifier used as 
        distribution of pIC50 values is clustered.
        
        :param df: Input dataframe of assay data
        :type df: pandas Dataframe
        :return: pandas Series
        """
        pIC50 = pd.Series(-np.log10(df[metric]))
        return (pIC50 > threshold)

"""Determines pIC50, using specified IC50 metric. Distribution of
        pIC50 values suggests we might was to use a classifier rather than
        regression here
        
        :param df: Input dataframe of assay data
        :type df: pandas Dataframe
        :return: pandas Series
        """

# This is a pretty simple one but you can come up with more useful stuff in RDKit