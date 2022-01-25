# Methods for analysing the data 

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

# This is a pretty simple one but you can come up with more useful stuff in RDKit