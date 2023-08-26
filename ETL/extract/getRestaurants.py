from ...DataExploration.secretKeys import maps_api_key
import requests


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
    if 'next_page_token' in results:
        next_page_token = results['next_page_token']
    return results, next_page_token


def get_next_page_nearby_search(token):
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
    params = {
        "pagetoken": token,
        "key": maps_api_key}

    r = requests.post(url, params=params)
    data = r.json()
    results = data['results']

    if 'next_page_token' in results:
        next_page_token = results['next_page_token']
    return results, next_page_token


def parse_nearby_search_result(results, census_id):
    mydict = {}
    name = [r['name'] for r in results]
    price_level = [r['price_level'] for r in results]
    place_id = [r['place_id'] for r in results]
    rating = [r['rating'] for r in results]
    user_ratings_total = [r['user_ratings_total'] for r in results]
    census_id = [census_id for r in results]

    mydict = {
        'name': name,
        'price_level': price_level,
        'place_id': place_id,
        'rating': rating,
        'user_ratings_total': user_ratings_total,
        'census_id': census_id
    }

    return mydict
