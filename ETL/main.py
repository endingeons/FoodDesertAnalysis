from getRestaurants import *
from read_csv import *
import os.path
from load import *

# Get lat, lon for each census tract
radius = 1609.344  # meters, 1 mile == 1609.344 meters
census_tract_ids = []
all_results = []

# Connect to SQL Database
connection = connect_local_sql_db()

# Create database if it doesn't exist
# execute_scripts_from_file(connection, 'create_restaurant_db.sql')

ATLAS_CSV_PATH = r'..\OriginalData\2019 Food Access Research Atlas Data\Food Access Research Atlas.csv'
CDC_CSV_PATH = r'..\OriginalData\PLACES__Local_Data_for_Better_Health__Census_Tract_Data_2023_release.csv'

OUTPUT_PATH = r'..\PreparedData'
exists_atlas = os.path.isfile(r'{}\food_atlas_data_nj.csv'.format(OUTPUT_PATH))
exists_cdc = os.path.isfile(r'{}\cdc_data_nj.csv'.format(OUTPUT_PATH))

# If PreparedData CSVs exist, don't run this code
if not(exists_atlas and exists_cdc):
    food_atlas_data = read_csv(ATLAS_CSV_PATH)
    cdc_data = read_csv(CDC_CSV_PATH)

    # Remove all non-NJ data
    filter_data(food_atlas_data, cdc_data)

    exists_atlas = os.path.isfile(r'{}\food_atlas_data_nj.csv'.format(OUTPUT_PATH))
    exists_cdc = os.path.isfile(r'{}\cdc_data_nj.csv'.format(OUTPUT_PATH))

# Check again if files were created
if exists_atlas and exists_cdc:
    food_atlas_data = read_csv(r'{}\food_atlas_data_nj.csv'.format(OUTPUT_PATH))
    cdc_data = read_csv(r'{}\cdc_data_nj.csv'.format(OUTPUT_PATH))

# Merge data on census_tract
merge_data = process_data(food_atlas_data, cdc_data)

# Insert Census Data
insert_census_data(connection, merge_data)

length_data = len(merge_data)

for index, row in merge_data.iterrows():
    print('{}/{}'.format(index+1, length_data))
    # Search census tract lat, lon
    results, next_page_token = nearby_search(row['census_lat'], row['census_lon'], radius)
    all_results = all_results + results

    while next_page_token:
        results, next_page_token = get_next_page_nearby_search(next_page_token)
        if next_page_token:
            all_results = all_results + results

    restaurant_dict = parse_nearby_search_result(all_results, row['CensusTract'])
    restaurant_df = pd.DataFrame(restaurant_dict)

    # Insert Restaurant Data
    print('Trying to insert restaurant data from census tract: {}'.format(row['CensusTract']))
    insert_restaurant_data(connection, restaurant_df)

# Close connection
close_local_sql_db(connection)

