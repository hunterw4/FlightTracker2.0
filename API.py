import requests
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()

class LocationSearch:
    API_KEY = os.environ.get("API_SECRET_KEY")
    endpoint = "https://api.unsplash.com/search/photos"
    def __init__(self, city):
        self.city = city

    def base_img(self):
        search_params = {
            "query": f"{self.city}",
            "per_page": 10,
            "client_id": LocationSearch.API_KEY
        }
        response = requests.get(LocationSearch.endpoint, params=search_params)
        data = response.json()
        query_img = data["results"][0]["urls"]["full"]
        return query_img

    def food_img(self):
        search_params = {
            "query": f"{self.city} food",
            "per_page": 10,
            "client_id": LocationSearch.API_KEY
        }
        response = requests.get(LocationSearch.endpoint, params=search_params)
        data = response.json()
        food_query = data["results"][0]["urls"]["full"]
        return food_query
    def architecture_img(self):
        search_params = {
            "query": f"{self.city} architecture",
            "per_page": 10,
            "client_id": LocationSearch.API_KEY
        }
        response = requests.get(LocationSearch.endpoint, params=search_params)
        data = response.json()
        architecture_query = data["results"][0]["urls"]["full"]
        return architecture_query



