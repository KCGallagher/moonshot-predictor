# Main script to execute analysis

from importer import import_data
from analyser import analyse_compounds, count_data_points
from analysis_methods import AnalysisMethods as am

def main():
    # Import data
    input_data = "data/activity_data.csv"
    df_assay, df_compounds = import_data(input_data)

    # Analyse data (and record in df_compounds)
    count_data_points(df_assay)
    df_compounds = analyse_compounds(df_assay, df_compounds, am.type_of_amide, 'amide')


if __name__ == '__main__':
    main()
    