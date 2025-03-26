import aiohttp
import requests
import os
import asyncio

class LocationSearch:
    API_KEY = os.environ.get("API_SECRET_KEY")
    endpoint = "https://api.unsplash.com/search/photos"
