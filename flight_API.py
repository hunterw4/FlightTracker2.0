import aiohttp
import requests
import os
from dotenv import load_dotenv, dotenv_values
from openai import OpenAI
import asyncio
from aiohttp import ClientSession
from datetime import datetime as dt, timedelta as td

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

    async def analyze_data(self, data):
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

class expensiveSearch():
    flightKey = "c93O3qnhnW-yd4wIQvkuDgsLjB_Jt_HW"
    url = "https://api.tequila.kiwi.com"

    def __init__(self, city):
        self.city = city
        self.header = {
            "apikey": expensiveSearch.flightKey
        }

    def IATA(self):
        iata_params = {
            "term": self.city
        }
        response = requests.get(url=f"{expensiveSearch.url}/locations/query", params=iata_params, headers=self.header)
        data = response.json()
        IATA = data["locations"][0]["id"]
        return IATA

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
            response = await session.get(url=f"{expensiveSearch.url}/v2/search", params=params, headers=self.header,
                                         ssl=False)
            data = await response.json()
            response.raise_for_status()  # Raise an error if the response is not successful
            new_data = await self.analyze_data(data)
        return new_data

    async def analyze_data(self, data):
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

        total_layover_hours = total_layover_time / 3600
        total_layover_hours_rounded = round(total_layover_hours)
        total_travel_time = total_layover_hours_rounded
        total_flight_hours = total_flight_time / 3600
        total_flight_hours_rounded = round(total_flight_hours)
        total_travel_time = total_flight_hours_rounded + total_layover_hours_rounded

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

    async def cheap_custom(self, IATA, IATA_TO, flight_type, num_days, fare, date, date_to, adults, children):
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
            "max_stopovers": 3,
            "stopover_from": "00:00",
            "stopover_to": "03:30",
            "curr": "USD",
        }
        async with aiohttp.ClientSession() as session:
            response = await session.get(url=f"{customSearch.url}/search", params=params, headers=self.header, ssl=False)
            data = await response.json()
            new_data = await self.analyze_data(data)
        return new_data

    async def expensive_custom(self, IATA, IATA_TO, flight_type, num_days, fare, date, date_to, adults, children):
        stop_to = "02:00"
        if children == None:
            children = 0
        if flight_type == "round":
            stop_to = "03:00"
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
            "stopover_to": stop_to,
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
        if data["data"][cheapest_index]["return_duration"]:
            # Adding the total flight time between outbound and return flights
            flight_return_time = data["data"][cheapest_index]["return_duration"]

            hours_minutes = total_flight_time.split('h')
            out_hours = int(hours_minutes[0])  # Convert the first part (hours) to an integer
            out_minutes = int(hours_minutes[1].split('m')[0])

            r_hours_minutes = flight_return_time.split('h')
            r_hours = int(r_hours_minutes[0])  # Convert the first part (hours) to an integer
            r_minutes = int(r_hours_minutes[1].split('m')[0])

            hours = out_hours + r_hours
            minutes = out_minutes + r_minutes
            if minutes > 60:
                hours += 1
                minutes -= 60

            total_flight_time = f"{hours}h {minutes}m"
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
                layover_time = max(layover_time, 0)  # Ensuring layover_time is non-negative
            # Add layover time to total layover
            total_layover_time += layover_time

        total_layover_hours = total_layover_time / 3600
        total_layover_hours_rounded = round(total_layover_hours)

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



