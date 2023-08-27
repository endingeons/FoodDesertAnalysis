from secretKeys import maps_api_key
import requests
from getNutrition import *


def nearby_search(lat, lon, radius):
    next_page_token = []
    typePlace = 'restaurant'
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
    params = {
        "location": "{},{}".format(lat, lon),
        "radius": radius,
        "type": typePlace,
        "key": maps_api_key
    }

    r = requests.post(url, params=params)
    data = r.json()
    results = data['results']
    if 'next_page_token' in data:
        next_page_token = data['next_page_token']
    return results, next_page_token


def get_next_page_nearby_search(token):
    next_page_token = []
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
    params = {
        "pagetoken": token,
        "key": maps_api_key}

    r = requests.post(url, params=params)
    data = r.json()
    results = data['results']

    if 'next_page_token' in data:
        next_page_token = data['next_page_token']
    return results, next_page_token


def parse_nearby_search_result(results, census_id):
    all_restaurants_dict = []

    # Only keep restaurants with a price level
    results = [r for r in results if 'price_level' in r]

    for r in results:
        # New food list
        food_list = []

        all_reviews = get_reviews(r['place_id'])
        review = ' '.join(all_reviews)

        food_list = detect_food_in_text(review)

        # If food list was generated, get the average nutrients for all food listed for current restaurant
        if food_list:
            food_list = list(set(food_list))
            if len(food_list) > 10:
                food_list = food_list[:10]
            avg_nutrition = get_average_nutrition(food_list)
            calories = avg_nutrition['calories']
            protein = avg_nutrition['protein']
            fat = avg_nutrition['fat']
            carbs = avg_nutrition['carbs']
        else:  # No nutritional information, all NaN
            continue

        all_restaurants_dict = all_restaurants_dict + \
                               [{'name': r['name'],
                                 'price_level': r['price_level'],
                                 'place_id': r['place_id'],
                                 'rating': r['rating'],
                                 'user_ratings_total': r['user_ratings_total'],
                                 'census_id': census_id,
                                 'avg_calories': calories,
                                 'avg_protein': protein,
                                 'avg_fat': fat,
                                 'avg_carbs': carbs
                                 }]

    return all_restaurants_dict


def get_reviews(place_id):
    url = 'https://maps.googleapis.com/maps/api/place/details/json?'
    params = {"fields": 'reviews',
              "place_id": place_id,
              "key": maps_api_key}

    result = requests.post(url, params=params)
    data = result.json()
    return [r['text'] for r in data['result']['reviews']]
