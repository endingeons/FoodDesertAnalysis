import pandas as pd
import re

def read_csv(csv_path):
    df = pd.read_csv(csv_path)
    return df


def filter_data(food_atlas_data, cdc_data):
    OUTPUT_PATH = r'..\\..\\PreparedData\\'

    food_atlas_data_flt = food_atlas_data[food_atlas_data['State'] == 'New Jersey']
    cdc_data_flt = cdc_data[cdc_data['StateAbbr'] == 'NJ']

    # Keep only necessary fields in filtered CSV
    # food_atlas_data['LILATracts_1And10']
    # food_atlas_data['Census Tract']
    # food_atlas_data['State']
    # food_atlas_data['County']

    # cdc_data['Location Id']
    # cdc_data['Geolocation']
    # cdc_data['StateAbbr']


    food_atlas_data_flt.to_csv('{}\\food_atlas_data_nj.csv'.format(OUTPUT_PATH))
    cdc_data_flt.to_csv('{}\\cdc_data_nj.csv'.format(OUTPUT_PATH))

def process_data(food_atlas_data, cdc_data):
    cdc_data.rename(columns={'Location Id': 'Census Tract'}, inplace=True)

    merge_data = food_atlas_data.join(cdc_data, on='Census Tract', how='left')

    latitude = [get_lat(x) for x in merge_data['Geolocation']]
    longitude = [get_lon(x) for x in merge_data['Geolocation']]

    # Combine latitude and longitude into dataframe

    return food_atlas_data, cdc_data

def get_lat(my_str):
    lat = re.findall('(?<=\()[-]*[\d.]*', my_str)[0]
    return lat


def get_lon(my_str):
    lon = re.findall('([-]*[\d.]*)(?=\))', my_str)[0]
    return lon
