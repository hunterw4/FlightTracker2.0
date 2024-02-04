import requests
import os
from dotenv import load_dotenv, dotenv_values
from openai import OpenAI


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
        return header_img
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
                    if tag.get("title", "").lower() == "food":
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

    def aiResponseP1(self):
        client = OpenAI(
            # This is the default and can be omitted
            api_key=openAi.openAiKey,
        )
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "You are providing information to a travel website, this paragraph needs to have a description of the requested city and what it has to offer and such with a max word count around 100"},
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
                 "content": "You are providing information to a travel website, this paragraph needs to provide information about culturaly relevant food items of the requested city and what its best known for. A max word cap around 100 words."},
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
                 "content": "You are providing information to a travel website. This paragraph needs to provide information about the architectual history of the requested city, what makes their architecture different and unique and some highlights of their architecture. Max word cap of around 100 words."},
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
                 "content": "You are providing information to a travel website. This needs to be a small catchy header for a already provided paragraph based off the requested city the existing paragraph goes into detail about the highlights of the requested city if that helps for context, also NO quotes"},
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
                 "content": "You are providing information to a travel website. This needs to be a small catchy header for a already provided paragraph based off the requested city the existing paragraph goes into detail about the culturaly rich food items of the city, also NO quotes"},
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
                 "content": "You are providing information to a travel website. This needs to be a small catchy header for a already provided paragraph based off the requested city the existing paragraph goes into detail about the highlights of the requested city's architecture if that helps for context, also NO quotes"},
                {"role": "user", "content": self.city}
            ]
        )

        h3_response = (completion.choices[0].message.content)
        return h3_response
