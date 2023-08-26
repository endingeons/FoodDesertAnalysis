from getRestaurants import *
from read_csv import *
import os.path

# Get lat, lon for each census tract
lat = 0
lon = 0
radius = 0
census_tract_ids = []
all_results = []

ATLAS_CSV_PATH = r'..\..\OriginalData\2019 Food Access Research Atlas Data/Food Access Research Atlas.csv'
CDC_CSV_PATH = r'..\..\OriginalData\PLACES__Local_Data_for_Better_Health__Census_Tract_Data_2023_release.csv'

# If PreparedData CSVs exist, don't run this code
OUTPUT_PATH = r'..\\..\\PreparedData\\'
exists_atlas = os.path.isfile('{}\\food_atlas_data_nj.csv'.format(OUTPUT_PATH))
exists_cdc = os.path.isfile('{}\\cdc_data_nj.csv'.format(OUTPUT_PATH))

if exists_atlas and exists_cdc:
    food_atlas_data = read_csv(ATLAS_CSV_PATH)
    cdc_data = read_csv(CDC_CSV_PATH)

    # Remove all non-NJ data
    filter_data(food_atlas_data, cdc_data)

process_data(food_atlas_data, cdc_data)

all_restaurant_dict = []

for lat, lon, census_id in census_tract_ids:
    # Search census tract lat, lon
    results, next_page_token = nearby_search(lat, lon, radius)
    all_results = all_results.append(results)

    while next_page_token:
        results, next_page_token = get_next_page_nearby_search(next_page_token)
        all_results = all_results.append(results)

    all_restaurant_dict = all_restaurant_dict.append(parse_nearby_search_result(all_results, census_id))

