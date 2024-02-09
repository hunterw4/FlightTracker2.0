from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import datetime
from API import LocationSearch, openAi
import asyncio
from aiohttp import ClientSession

app = Flask(__name__)

Bootstrap5(app)

@app.route("/", methods=["GET", "POST"])
def home():
    flights = ["Palermo", "Berlin", "Abu Dhabi"]
    cities = ["Paris", "Venice", "Tokyo", "Kyoto", "Rome", "Milan", "Florence"]
    flight_list = []
    poi_list = []
    for city in cities:
        locationsearch = LocationSearch(city)
        poi_img = locationsearch.header_img()
        poi_list.append((city, poi_img))
    for city in flights:
        locationsearch = LocationSearch(city)
        flight_img = locationsearch.header_img()
        flight_list.append((city, flight_img))
    return render_template("index.html", poi_list=poi_list, flight_list=flight_list)

    # if request.method == "POST":
    #     city = request.form["city"]
    #     locationsearch = LocationSearch(city)
    #     poi_img = locationsearch.base_img()
    #     poi_list = []
    #     poi_list.append((city, poi_img))
    #     return render_template("index.html", poi_list=poi_list)

# Current load time is 20 seconds

async def imgQuery(city):
    locationsearch = LocationSearch(city)
    header_img = locationsearch.header_img()
    base_img = locationsearch.base_img()
    food_img = locationsearch.food_img()
    architecture_img = locationsearch.architecture_img()
    return header_img, base_img, food_img, architecture_img

async def aIQuery(city):
    gpt = openAi(city)
    country = gpt.aiResponseCountry()
    dynamic_p1 = gpt.aiResponseP1()
    dynamic_p2 = gpt.aiResponseP2()
    dynamic_p3 = gpt.aiResponseP3()
    dynamic_h1 = gpt.aiResponseH1()
    dynamic_h2 = gpt.aiResponseH2()
    dynamic_h3 = gpt.aiResponseH3()

    return country, dynamic_p1, dynamic_p2, dynamic_p3, dynamic_h1, dynamic_h2, dynamic_h3

# Current load time is 20 seconds
@app.route("/search", methods=["GET", "POST"])
async def search():
    if request.method == "POST":
        city = request.form["search"]
        ai_result = await aIQuery(city)
        img_result = await imgQuery(city)

        header_img, base_img, food_img, architecture_img = img_result
        country, dynamic_p1, dynamic_p2, dynamic_p3, dynamic_h1, dynamic_h2, dynamic_h3 = ai_result

    return render_template("search.html", city=city, header_img=header_img, base_img=base_img, food_img=food_img,
                               architecture_img=architecture_img, country=country, dynamic_p1=dynamic_p1, dynamic_p2=dynamic_p2, dynamic_p3=dynamic_p3, dynamic_h1=dynamic_h1,
                                dynamic_h2=dynamic_h2, dynamic_h3=dynamic_h3)

if __name__ == "__main__":
    app.run(debug=True)


