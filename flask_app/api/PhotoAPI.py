from platform import architecture

import aiohttp
import requests
import os
import asyncio
import aiohttp

class PhotoSearch:
    API_KEY = os.environ.get("API_SECRET_KEY")
    ENDPOINT = "https://api.unsplash.com/search/photos"
    def __init__(self, city, country):
        self.city = city
        self.country = country


    async def carsoul_imgs(self):
        search_params = {
            "query": f"{self.city}",
            "per_page": 10,
            "client_id": PhotoSearch.API_KEY
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(self.ENDPOINT, params=search_params) as response:
                data = await response.json()
                c_img = data["results"][0]["urls"]["full"]
                c_img2 = data['results'][2]['urls']['full']
                c_img3 = data['results'][3]['urls']['full']
                return c_img, c_img2, c_img3

    async def header_img(self):
        search_params = {
            "query": f"{self.city}",
            "per_page": 10,
            "client_id": PhotoSearch.API_KEY
        }

        async with aiohttp.ClientSession() as session:
           async with session.get(self.ENDPOINT, params=search_params) as response:
               data = await response.json()
               header_img = data['results'][1]['urls']['full']
               return header_img




    async def food_img(self):
        search_params = {
            "query": f"{self.city} food",
            "per_page": 5,
            "client_id": PhotoSearch.API_KEY
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(self.ENDPOINT, params=search_params) as response:
                data = await response.json()
                food_img = data['results'][0]['urls']['full']
                return food_img


    async def architecture_img(self):
        search_params = {
            "query": f"{self.city} architecture",
            "per_page": 5,
            "client_id": PhotoSearch.API_KEY
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(self.ENDPOINT, params=search_params) as response:
                data = await response.json()
                architecture = data['results'][0]['urls']['full']
                return architecture

    async def main(self):
        tasks = [
            self.carsoul_imgs(),
            self.header_img(),
            self.food_img(),
            self.architecture_img()
        ]

        results = await asyncio.gather(*tasks)
        c_img, c_img2, c_img3 = results[0]
        header_img = results[1]
        food_img = results[2]
        arch_img = results[3]
        return c_img, c_img2, c_img3, header_img, food_img, arch_img