import pandas as pd
import re


def read_csv(csv_path):
    df = pd.read_csv(csv_path)
    return df


def filter_data(food_atlas_data, cdc_data):
    OUTPUT_PATH = r'..\\..\\PreparedData\\'

    food_atlas_data_flt = food_atlas_data[food_atlas_data['State'] == 'New Jersey']
    cdc_data_flt = cdc_data[cdc_data['StateAbbr'] == 'NJ']

    food_atlas_data_flt.to_csv('{}\\food_atlas_data_nj.csv'.format(OUTPUT_PATH), index=False, index_label=None)
    cdc_data_flt.to_csv('{}\\cdc_data_nj.csv'.format(OUTPUT_PATH), index=False, index_label=None)


def process_data(food_atlas_data, cdc_data):
    cdc_data.rename(columns={'LocationID': 'CensusTract'}, inplace=True)
    cdc_data = cdc_data[['CensusTract', 'Geolocation']].drop_duplicates()
    print('Excluded census tract ids:')
    print(set(food_atlas_data['CensusTract']) ^ set(cdc_data['CensusTract']))

    merge_data = food_atlas_data.merge(cdc_data,
                                       on='CensusTract',
                                       how='inner',
                                       )

    latitude = [float(get_lat(x)) for x in merge_data['Geolocation']]
    longitude = [float(get_lon(x)) for x in merge_data['Geolocation']]

    # Combine latitude and longitude into dataframe
    merge_data['census_lat'] = latitude
    merge_data['census_lon'] = longitude

    return merge_data


def get_lat(my_str):
    lat = re.findall(r'([-]*[\d.]*)(?=\))', my_str)[0]
    return lat


def get_lon(my_str):
    lon = re.findall(r'(?<=\()[-]*[\d.]*', my_str)[0]
    return lon
