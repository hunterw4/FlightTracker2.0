import aiohttp
import requests
import os
from dotenv import load_dotenv, dotenv_values
from openai import OpenAI
import asyncio
from aiohttp import ClientSession
from datetime import datetime as dt, timedelta as td

load_dotenv()

class LocationSearch:
    API_KEY = os.environ.get("API_SECRET_KEY")
    endpoint = "https://api.unsplash.com/search/photos"
    def __init__(self, city):
        self.city = city
    def header_img(self):
        search_params = {
            "query": f"{self.city}",
            "per_page": 10,
            "client_id": LocationSearch.API_KEY
        }
        response = requests.get(LocationSearch.endpoint, params=search_params)
        data = response.json()
        header_img = data["results"][0]["urls"]["full"]
        # base_img is [1] hence the skip
        header_img2 = data["results"][2]["urls"]["full"]
        header_img3 = data["results"][3]["urls"]["full"]
        return header_img, header_img2, header_img3
    def base_img(self):
        search_params = {
            "query": f"{self.city}",
            "per_page": 10,
            "client_id": LocationSearch.API_KEY
        }
        response = requests.get(LocationSearch.endpoint, params=search_params)
        data = response.json()
        query_img = data["results"][1]["urls"]["full"]
        return query_img

    def food_img(self):
        search_params = {
            "query": f"{self.city} food",
            "per_page": 10,
            "client_id": LocationSearch.API_KEY
        }
        response = requests.get(LocationSearch.endpoint, params=search_params)
        data = response.json()
        for photo in data["results"]:
            if "tags" in photo:
                for tag in photo["tags"]:
                    if tag.get("title", "").lower() == "food" and tag.get("title", "").lower() == f"{self.city}":
                        return photo["urls"]["full"]
        #If no food photo is found, return first URL
        return data["results"][0]["urls"]["full"]
    def architecture_img(self):
        search_params = {
            "query": f"{self.city} architecture",
            "per_page": 10,
            "client_id": LocationSearch.API_KEY
        }
        response = requests.get(LocationSearch.endpoint, params=search_params)
        data = response.json()
        for photo in data["results"]:
            if "tags" in photo:
                for tag in photo["tags"]:
                    if tag.get("title", "").lower() == "architecture" and tag.get("title", "").lower() == f"{self.city}":
                        return photo["urls"]["full"]
        #If no food photo is found, return first URL
        return data["results"][0]["urls"]["full"]
        architecture_query = data["results"][0]["urls"]["full"]
        return architecture_query

class openAi:
    openAiKey = os.environ.get("OPENAI_KEY")
    def __init__(self, city):
        self.city = city
    def aiResponseCountry(self):
        client = OpenAI(
            # This is the default and can be omitted
            api_key=openAi.openAiKey,
        )
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                    "content": "You are matching the country to the requested city, match it as best as possible but only reply with a country no extra text or explanations even if you cant find it"},
                {"role": "user", "content": self.city}
            ]
        )

        country_response = (completion.choices[0].message.content)
        return country_response

    def aiResponseAirport(self):
        client = OpenAI(
            # This is the default and can be omitted
            api_key=openAi.openAiKey,
        )
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                    "content": "ONLY RESPOND WITH ONE WORD. Based off the city entered by the user return the city with the nearest airport to it, so if Tokyo has one then it would be Tokyo if Kyoto doesnt have one return the closest city that does ONLY ONE WORD WHICH WILL BE THE CITY"},
                {"role": "user", "content": self.city}
            ]
        )

        airport_response = (completion.choices[0].message.content)
        return airport_response

    def aiResponseP1(self):
        client = OpenAI(
            # This is the default and can be omitted
            api_key=openAi.openAiKey,
        )
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "You are providing information to a travel website, this paragraph needs to have a description of the requested city and what it has to offer and such with a max word count between 50-75 whichever is most natural for the paragraph"},
                {"role": "user", "content": self.city}
            ]
        )

        p1_response = (completion.choices[0].message.content)
        return p1_response

    def aiResponseP2(self):
        client = OpenAI(
            # This is the default and can be omitted
            api_key=openAi.openAiKey,
        )
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "You are providing information to a travel website, this paragraph needs to provide information about culturaly relevant food items of the requested city and what its best known for. max word count between 50-75 whichever is most natural for the paragraph."},
                {"role": "user", "content": self.city}
            ]
        )

        p2_response = (completion.choices[0].message.content)
        return p2_response

    def aiResponseP3(self):
        client = OpenAI(
            # This is the default and can be omitted
            api_key=openAi.openAiKey,
        )
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "You are providing information to a travel website. This paragraph needs to provide information about the architectual history of the requested city, what makes their architecture different and unique and some highlights of their architecture. max word count between 50-75 whichever is most natural for the paragraph."},
                {"role": "user", "content": self.city}
            ]
        )

        p3_response = (completion.choices[0].message.content)
        return p3_response

    def aiResponseH1(self):
        client = OpenAI(
            # This is the default and can be omitted
            api_key=openAi.openAiKey,
        )
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "You are providing information to a travel website. This needs to be a small catchy header max word count between 6-8 words for a already provided paragraph based off the requested city the existing paragraph goes into detail about the highlights of the requested city if that helps for context, also NO quotes, do not put quotes for the header it interferes with my program"},
                {"role": "user", "content": self.city}
            ]
        )

        h1_response = (completion.choices[0].message.content)
        return h1_response

    def aiResponseH2(self):
        client = OpenAI(
            # This is the default and can be omitted
            api_key=openAi.openAiKey,
        )
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "You are providing information to a travel website. This needs to be a small catchy header max word count between 6-8 words for a already provided paragraph based off the requested city the existing paragraph goes into detail about the culturaly rich food items of the city, also NO quotes, do not put quotes for the header it interferes with my program"},
                {"role": "user", "content": self.city}
            ]
        )

        h2_response = (completion.choices[0].message.content)
        return h2_response

    def aiResponseH3(self):
        client = OpenAI(
            # This is the default and can be omitted
            api_key=openAi.openAiKey,
        )
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "You are providing information to a travel website. This needs to be a small catchy header max word count between 6-8 words for a already provided paragraph based off the requested city the existing paragraph goes into detail about the highlights of the requested city's architecture if that helps for context, also NO quotes, do not put quotes for the header it interferes with my program"},
                {"role": "user", "content": self.city}
            ]
        )

        h3_response = (completion.choices[0].message.content)
        return h3_response

class flightSearch():
    flightKey = "c93O3qnhnW-yd4wIQvkuDgsLjB_Jt_HW"
    url = "https://api.tequila.kiwi.com"

    def __init__(self, city):
        self.city = city
        self.header = {
            "apikey": flightSearch.flightKey
        }

    def IATA(self):
        iata_params = {
            "term": self.city
        }
        response = requests.get(url=f"{flightSearch.url}/locations/query", params=iata_params, headers=self.header)
        data = response.json()
        IATA = data["locations"][0]["id"]
        return IATA
    async def cheapest_search(self, IATA):
        date = dt.now().strftime("%d/%m/%Y")
        six_month = dt.now() + td(days=+ 180)
        date_to = six_month.strftime("%d/%m/%Y")
        params = {
            "fly_from": "BOI",
            "fly_to": IATA,
            "date_from": date,
            "date_to": date_to,
            "select_airlines": "NK",
            "select_airlines_exclude": "True",
            "adults": 1,
            "children": 0,
            "max_stopovers": 4,
            "stopover_from": "00:00",
            "stopover_to": "04:00",
            "curr": "USD",

        }
        async with aiohttp.ClientSession() as session:
            response = await session.get(url=f"{flightSearch.url}/v2/search", params=params, headers=self.header, ssl=False)
            data = await response.json()
        new_data = await self.analyze_data(data)
        return new_data



    async def average_search(self, IATA):
        date = dt.now().strftime("%d/%m/%Y")
        six_month = dt.now() + td(days=+ 180)
        date_to = six_month.strftime("%d/%m/%Y")
        params = {
            "fly_from": "BOI",
            "fly_to": IATA,
            "date_from": date,
            "date_to": date_to,
            "select_airlines": "NK",
            "select_airlines_exclude": "True",
            "adults": 1,
            "children": 0,
            "max_stopovers": 2,
            "stopover_from": "00:00",
            "stopover_to": "04:00",
            "curr": "USD",

        }
        async with aiohttp.ClientSession() as session:
            response = await session.get(url=f"{flightSearch.url}/v2/search", params=params, headers=self.header, ssl=False)
            data = await response.json()
        new_data = await self.analyze_data(data)
        return new_data


    async def expensive_search(self, IATA):
        date = dt.now().strftime("%d/%m/%Y")
        six_month = dt.now() + td(days=+ 180)
        date_to = six_month.strftime("%d/%m/%Y")
        params = {
            "fly_from": "BOI",
            "fly_to": IATA,
            "date_from": date,
            "date_to": date_to,
            "selected_cabins": "C",
            "mix_with_cabins": "F",
            "select_airlines": "NK",
            "select_airlines_exclude": "True",
            "adults": 1,
            "children": 0,
            "max_stopovers": 2,
            "stopover_from": "00:00",
            "stopover_to": "04:00",
            "curr": "USD",

        }
        async with aiohttp.ClientSession() as session:
            response = await session.get(url=f"{flightSearch.url}/v2/search", params=params, headers=self.header, ssl=False)
            data = await response.json()
        new_data = await self.analyze_data(data)
        return new_data

    async def analyze_data(self, data):
        if not data or "data" not in data or not data["data"]:
            IATA = self.IATA()
            data = await self.average_search(IATA)
            if not data or "data" not in data or not data["data"]:
                IATA = self.IATA()
                data = await self.cheapest_search(IATA)
                if not data or "data" not in data or not data["data"]:
                    # Handle the case where all the search fails
                    return None, None, None, None, None, None

        cheapest = float('inf')  # Initialize with positive infinity so that any price will be lower
        cheapest_index = None
        deep_link = ""
        total_layover_time = 0
        total_flight_time = 0
        for i, flight_data in enumerate(data["data"]):
            price = flight_data["price"]
            if price < cheapest:
                cheapest = price
                cheapest_index = i
        stop = data["data"][cheapest_index]["route"]
        for i in range(len(stop) - 1):  # Stop iterating at the second-to-last segment
            current_flight_arrival = stop[i]['utc_arrival']
            next_flight_departure = stop[i + 1]['utc_departure']

            # Convert departure and arrival times to datetime objects for calculation
            current_flight_arrival_dt = dt.strptime(current_flight_arrival, "%Y-%m-%dT%H:%M:%S.%fZ")
            next_flight_departure_dt = dt.strptime(next_flight_departure, "%Y-%m-%dT%H:%M:%S.%fZ")

            # Calculate layover time between consecutive flights
            layover_time = (next_flight_departure_dt - current_flight_arrival_dt).total_seconds()

            # Add layover time to total layover
            total_layover_time += layover_time

            # Calculate flight time for the current segment
            flight_time = (next_flight_departure_dt - current_flight_arrival_dt).total_seconds()

            # Add flight time to total flight time
            total_flight_time += flight_time

            # Convert total layover time to hours and round up
        total_layover_hours = total_layover_time / 3600
        total_layover_hours_rounded = round(total_layover_hours)

        # Convert total flight time to hours and round up
        total_flight_hours = total_flight_time / 3600
        total_flight_hours_rounded = round(total_flight_hours)
        total_travel_time = total_flight_hours_rounded + total_layover_hours_rounded

        # Print total layover time after the loop
        fare = stop[0]["fare_category"]
        flight_class = ""
        if fare == "M":
            flight_class = "Economy"
        elif fare == "C":
            flight_class = "Business"
        elif fare == "F":
            flight_class = "First Class"
        stops = len(stop) - 1

        deep_link = data["data"][cheapest_index]["deep_link"]

        return cheapest, flight_class, stops, total_layover_hours_rounded, total_travel_time, deep_link


    # async def custom_search(self):
    #     params = {
    #         "fly_from": "boise"
    #     }
    #     async with aiohttp.ClientSession() as session:
    #         response = await session.get(url=f"{flightSearch.url}/search", params=params, headers=self.header)
    #         data = await response.json()


