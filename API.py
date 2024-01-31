import requests


class LocationSearch():
    def __init__(self):
        self.API_KEY = "secret"
        self.endpoint = "https://api.unsplash.com/search/photos"

    def imageSearch(self, location):
        search_params = {
            "query": location,
            "client_id": self.API_KEY
        }
        response = requests.get(self.endpoint, params=search_params)
        print(response)

#Still not sure why this isnt working ^^