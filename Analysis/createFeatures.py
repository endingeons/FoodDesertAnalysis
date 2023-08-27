# local imports
import sys
sys.path.append('../')
from ETL.load import *
import pandas as pd
from statistics import mean


def create_features():
    census_tract_id = []
    LILATract_1And10 = []
    state = []
    county = []
    num_restaurants = []
    min_calories = []
    max_calories = []
    mean_calories = []
    min_protein = []
    max_protein = []
    mean_protein = []
    min_fat = []
    max_fat = []
    mean_fat = []
    min_carbs = []
    max_carbs = []
    mean_carbs = []
    num_price_level_1 = []
    num_price_level_2 = []
    num_price_level_3 = []
    num_price_level_4 = []
    num_rating_less_2 = []
    num_rating_2_to_4 = []
    num_rating_great_4 = []
    avg_rating_total = []
    total_ratings_count = []

    # Connect to SQL Database
    connection = connect_local_sql_db()

    restaurant_tuples = execute_query_fetchall(connection, 'SELECT * FROM fooddesert.restaurant')
    census_tract_tuples = execute_query_fetchall(connection, """
                                                    SELECT * FROM fooddesert.census_tract ct
                                                    WHERE ct.census_tract_id 
                                                    IN (SELECT DISTINCT census_tract_id FROM restaurant);
                                                 """)
    # Close connection
    close_local_sql_db(connection)

    for row in census_tract_tuples:
        census_tract_id = census_tract_id + [row[0]]
        LILATract_1And10 = LILATract_1And10 + [row[1]]
        state = state + [row[2]]
        county = county + [row[3]]

    for curr_id in census_tract_id:
        """
            restaurant_key, place_id, restaurant_name, census_tract_id, price_level, rating, \
            user_rating_total, avg_calories, avg_protein, avg_fat, avg_carbs
        """
        tuple_filt = [t for t in restaurant_tuples if curr_id == t[3]]
        num_restaurants = num_restaurants + [len(tuple_filt)]
        # Calories
        min_calories = min_calories + [min([float(t[7]) for t in tuple_filt])]
        max_calories = max_calories + [max([float(t[7]) for t in tuple_filt])]
        mean_calories = mean_calories + [mean([float(t[7]) for t in tuple_filt])]
        # Protein
        min_protein = min_protein + [min([float(t[8]) for t in tuple_filt])]
        max_protein = max_protein + [max([float(t[8]) for t in tuple_filt])]
        mean_protein = mean_protein + [mean([float(t[8]) for t in tuple_filt])]
        # Fat
        min_fat = min_fat + [min([float(t[9]) for t in tuple_filt])]
        max_fat = max_fat + [max([float(t[9]) for t in tuple_filt])]
        mean_fat = mean_fat + [mean([float(t[9]) for t in tuple_filt])]
        # Carbs
        min_carbs = min_carbs + [min([float(t[10]) for t in tuple_filt])]
        max_carbs = max_carbs + [max([float(t[10]) for t in tuple_filt])]
        mean_carbs = mean_carbs + [mean([float(t[10]) for t in tuple_filt])]
        # Price Level $ - $$$$
        num_price_level_1 = num_price_level_1 + [len([t for t in tuple_filt if t[4] == 1])]
        num_price_level_2 = num_price_level_2 + [len([t for t in tuple_filt if t[4] == 2])]
        num_price_level_3 = num_price_level_3 + [len([t for t in tuple_filt if t[4] == 3])]
        num_price_level_4 = num_price_level_4 + [len([t for t in tuple_filt if t[4] == 4])]
        # Rating from 1 - 5 stars
        num_rating_less_2 = num_rating_less_2 + [len([t for t in tuple_filt if t[5] <= 2])]
        num_rating_2_to_4 = num_rating_2_to_4 + [len([t for t in tuple_filt if t[5] > 2 or t[5] <= 4])]
        num_rating_great_4 = num_rating_great_4 + [len([t for t in tuple_filt if t[5] > 4])]
        # Average Rating
        avg_rating_total = avg_rating_total + [mean([float(t[5]) for t in tuple_filt])]
        # Total Ratings Count
        total_ratings_count = total_ratings_count + [sum([float(t[6]) for t in tuple_filt])]

    features_dict = {
        'census_tract_id': census_tract_id,
        'LILATract_1And10': LILATract_1And10,
        'state': state,
        'county': county,
        'num_restaurants': num_restaurants,
        'min_calories': min_calories,
        'max_calories': max_calories,
        'mean_calories': mean_calories,
        'min_protein': min_protein,
        'max_protein': max_protein,
        'mean_protein': mean_protein,
        'min_fat': min_fat,
        'max_fat': max_fat,
        'mean_fat': mean_fat,
        'min_carbs': min_carbs,
        'max_carbs': max_carbs,
        'mean_carbs': mean_carbs,
        'num_price_level_1': num_price_level_1,
        'num_price_level_2': num_price_level_2,
        'num_price_level_3': num_price_level_3,
        'num_price_level_4': num_price_level_4,
        'num_rating_less_2': num_rating_less_2,
        'num_rating_2_to_4': num_rating_2_to_4,
        'num_rating_great_4': num_rating_great_4,
        'avg_rating_total': avg_rating_total,
        'total_ratings_count': total_ratings_count
    }
    df = pd.DataFrame(features_dict)
    return df

