import aiohttp
import requests
import os
from dotenv import load_dotenv, dotenv_values
from openai import OpenAI
import asyncio
from aiohttp import ClientSession
from datetime import datetime as dt, timedelta as td

class customSearch():
    flightKey = "c93O3qnhnW-yd4wIQvkuDgsLjB_Jt_HW"
    url = "https://api.tequila.kiwi.com"

    def __init__(self, city, city_to):
        self.city = city
        self.city_to = city_to
        self.header = {
            "apikey": customSearch.flightKey
        }

    def IATA(self):
        iata_params = {
            "term": self.city
        }
        response = requests.get(url=f"{customSearch.url}/locations/query", params=iata_params, headers=self.header)
        data = response.json()
        IATA = data["locations"][0]["id"]
        return IATA

    def IATA_TO(self):
        iata_params = {
            "term": self.city_to
        }
        response = requests.get(url=f"{customSearch.url}/locations/query", params=iata_params, headers=self.header)
        data = response.json()
        IATA = data["locations"][0]["id"]
        return IATA

    async def cheap_custom(self, IATA, IATA_TO, fare, date, date_to, adults, children):
        if children == None:
            children = 0
        params = {
            "fly_from": IATA,
            "fly_to": IATA_TO,
            "date_from": date,
            "date_to": date_to,
            "nights_in_dst_from": num_days,
            "nights_in_dst_to": num_days,
            "selected_cabins": fare,
            "select_airlines": "NK",
            "select_airlines_exclude": "True",
            "adults": adults,
            "children": children,
            "max_stopovers": 4,
            "stopover_from": "00:00",
            "stopover_to": "04:00",
            "curr": "USD",
        }
        async with aiohttp.ClientSession() as session:
            response = await session.get(url=f"{customSearch.url}/search", params=params, headers=self.header, ssl=False)
            data = await response.json()
            new_data = await self.analyze_data(data)
        return new_data

    async def average_custom(self, IATA, IATA_TO, flight_type, num_days, fare, date, date_to, adults, children):
        if children == None:
            children = 0
        params = {
            "fly_from": IATA,
            "fly_to": IATA_TO,
            "date_from": date,
            "date_to": date_to,
            "nights_in_dst_from": num_days,
            "nights_in_dst_to": num_days,
            "selected_cabins": fare,
            "typeFlight": flight_type,
            "select_airlines": "NK",
            "select_airlines_exclude": "True",
            "adults": adults,
            "children": children,
            "max_stopovers": 2,
            "stopover_from": "00:00",
            "stopover_to": "04:00",
            "curr": "USD",
        }
        async with aiohttp.ClientSession() as session:
            response = await session.get(url=f"{customSearch.url}/search", params=params, headers=self.header, ssl=False)
            data = await response.json()
            new_data = await self.analyze_data(data)
        return data

    async def expensive_custom(self, IATA, IATA_TO, fare, date, date_to, adults, children):
        if children == None:
            children = 0
        params = {
            "fly_from": IATA,
            "fly_to": IATA_TO,
            "date_from": date,
            "date_to": date_to,
            "selected_cabins": fare,
            "select_airlines": "NK",
            "select_airlines_exclude": "True",
            "adults": adults,
            "children": children,
            "max_stopovers": 2,
            "stopover_from": "00:00",
            "stopover_to": "04:00",
            "curr": "USD",
        }
        async with aiohttp.ClientSession() as session:
            response = await session.get(url=f"{customSearch.url}/search", params=params, headers=self.header, ssl=False)
            data = await response.json()
            new_data = await self.analyze_data(data)
        return new_data

    async def analyze_data(self, data):
        cheapest = float('inf')  # Initialize with positive infinity so that any price will be lower
        cheapest_index = None
        deep_link = ""
        total_layover_time = 0
        for i, flight_data in enumerate(data["data"]):
            price = flight_data["price"]
            if price < cheapest:
                cheapest = price
                cheapest_index = i
        stop = data["data"][cheapest_index]["route"]
        total_flight_time = data["data"][cheapest_index]["fly_duration"]
        for i in range(len(stop) - 1):  # Stop iterating at the second-to-last segment
            current_flight_arrival = stop[i]['aTimeUTC']
            next_flight_departure = stop[i + 1]['dTimeUTC']

            current_flight_arrival_dt = dt.utcfromtimestamp(current_flight_arrival)
            next_flight_departure_dt = dt.utcfromtimestamp(next_flight_departure)

            # Calculate layover time between consecutive flights
            layover_time = (next_flight_departure_dt - current_flight_arrival_dt).total_seconds()
            if data["data"][cheapest_index]["nightsInDest"]:
                days = data["data"][cheapest_index]["nightsInDest"]
                time_in_dest = days * 24 * 60 * 60
                layover_time -= time_in_dest
            # Add layover time to total layover
            total_layover_time += layover_time

        total_layover_hours = total_layover_time / 3600
        total_layover_hours_rounded = round(total_layover_hours)
        total_travel_time = total_layover_hours_rounded

        fare = stop[0]["fare_category"]
        flight_class = ""
        if fare == "M":
            flight_class = "Economy"
        elif fare == "C":
            flight_class = "Business"
        elif fare == "F":
            flight_class = "First Class"
        stops = len(stop) - 1
        if stops == 0:
            stops = "Zero"

        deep_link = data["data"][cheapest_index]["deep_link"]
        return cheapest, flight_class, stops, total_layover_hours_rounded, total_flight_time, deep_link


async def main():
    city = ""
    city_to = "tokyo"
    raw_depart = "28/02/2024"
    raw_return = "05/03/2024"
    fare = "M"
    flight_type = "round"
    adults = 1
    children = 0
    num_days = 7

    flight = customSearch(city, city_to)
    IATA = flight.IATA()
    IATA_TO = flight.IATA_TO()

    test = await flight.average_custom(IATA,IATA_TO, flight_type, num_days,fare,raw_depart,raw_return,adults,children)
    print(test)

asyncio.run(main())