import spoonacular as sp
from secretKeys import api_key
from statistics import mean
import time


def detect_food_in_text(review_sample):
    time.sleep(0.2)  # Rate limited to 5 requests per s
    api = connect_to_spoonacular()
    response = api.detect_food_in_text(review_sample)
    data = response.json()
    return [x['annotation'] for x in data['annotations'] if x['tag'] == 'dish']

    # return ['potato', 'tomato']


def get_average_nutrition(food_list):
    api = connect_to_spoonacular()
    calories = []
    fat = []
    protein = []
    carbs = []

    for food in food_list:
        # time.sleep(0.2)  # Rate limited to 5 requests per s
        response = api.guess_nutrition_by_dish_name(food)
        data = response.json()
        calories.append(data['calories']['value'])
        fat.append(data['fat']['value'])
        protein.append(data['protein']['value'])
        carbs.append(data['carbs']['value'])

    return {
        'calories': mean(calories),
        'fat': mean(fat),
        'protein': mean(protein),
        'carbs': mean(carbs)
    }
    # return {
    #     'calories': 1,
    #     'fat': 1,
    #     'protein': 1,
    #     'carbs': 1}


def connect_to_spoonacular():
    # Connect to API
    return sp.API(api_key)

