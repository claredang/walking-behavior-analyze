import xml.etree.ElementTree as ET
import pandas as pd

def analysis_data(filename):
    # Create element tree object
    tree = ET.parse(filename) 
    root = tree.getroot()

    records = [i.attrib for i in root.iter("Record")]

    # Change time format
    records_df = pd.DataFrame(records)
    date_col = ['creationDate', 'startDate', 'endDate']
    records_df[date_col] = records_df[date_col].apply(pd.to_datetime)

    # Extract only Walking asymmetric information
    walking_asymmetric_df = records_df.query("type == 'HKQuantityTypeIdentifierWalkingAsymmetryPercentage'")

    # # Print all categories
    # column_headers = list(walking_asymmetric_df.columns.values)
    # print("Categories :", column_headers)

    # Drop unncesssary categories
    walking_asymmetric_df.drop(['type', 'sourceVersion', 'unit', 'device'], axis=1, inplace=True)

    # Extract only the latest year
    walking_asymmetric_latest_year = walking_asymmetric_df[walking_asymmetric_df['startDate'].dt.strftime('%Y') == '2022']

    # Extract data since October
    # walking_asymmetric_latest_year = walking_asymmetric_df[walking_asymmetric_df['startDate'].dt.strftime('%Y-%m') == '2022-10']
    # print("Latest year: ", walking_asymmetric_latest_year)

    # Change string type to float type for 'value'
    walking_asymmetric_latest_year['value'] = pd.to_numeric(walking_asymmetric_latest_year['value'], downcast="float")

    # Find mean
    walking_asymmetric_average = walking_asymmetric_latest_year['value'].mean(axis=0) * 100
    # print("Walking asymmetric in % latest year: ", walking_asymmetric_average)

    return walking_asymmetric_average