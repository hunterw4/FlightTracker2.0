import aiohttp
import requests
import os
from openai import OpenAI
import asyncio
from datetime import datetime as dt, timedelta as td

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


    # async def custom_search(self, IATA, fly_from, date, date_to, fare, adults, children):
    #      params = {
    #         "fly_from": fly_from,
    #         "fly_to": IATA,
    #         "date_from": date,
    #         "date_to": date_to,
    #         "selected_cabins": fare,
    #         "select_airlines": "NK",
    #         "select_airlines_exclude": "True",
    #         "adults": adults,
    #         "children": children,
    #         "max_stopovers": 2,
    #         "stopover_from": "00:00",
    #         "stopover_to": "04:00",
    #         "curr": "USD",
    #
    #     }
    #      async with aiohttp.ClientSession() as session:
    #          response = await session.get(url=f"{flightSearch.url}/search", params=params, headers=self.header)
    #          data = await response.json()
    #          new_data = await self.anylyze_data(data)
    #          return cheapest, flight_class, stops, total_layover_hours_rounded, total_travel_time, deep_link