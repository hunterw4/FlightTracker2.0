from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import datetime
from API import LocationSearch, openAi, flightSearch
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
        poi_img = locationsearch.base_img()
        poi_list.append((city, poi_img))
    for city in flights:
        locationsearch = LocationSearch(city)
        flight_img = locationsearch.base_img()
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
    header_img, header_img2, header_img3 = locationsearch.header_img()
    base_img = locationsearch.base_img()
    food_img = locationsearch.food_img()
    architecture_img = locationsearch.architecture_img()
    return header_img, header_img2, header_img3, base_img, food_img, architecture_img

async def aIQuery(city):
    gpt = openAi(city)
    country = gpt.aiResponseCountry()
    airport = gpt.aiResponseAirport()
    dynamic_p1 = gpt.aiResponseP1()
    dynamic_p2 = gpt.aiResponseP2()
    dynamic_p3 = gpt.aiResponseP3()
    dynamic_h1 = gpt.aiResponseH1()
    dynamic_h2 = gpt.aiResponseH2()
    dynamic_h3 = gpt.aiResponseH3()

    return country, airport, dynamic_p1, dynamic_p2, dynamic_p3, dynamic_h1, dynamic_h2, dynamic_h3


async def fetch_flight_data(airport, search_func):
    flightsearch = flightSearch(airport)
    IATA = flightsearch.IATA()
    data = await search_func(IATA)
    return (data[0], data[1], data[2], data[3], data[4], data[5])  # Return flight data as a tuple


# Current load time is 20 seconds
@app.route("/search", methods=["GET", "POST"])
async def search():
    if request.method == "POST":
        city = request.form["search"]
        ai_result = await aIQuery(city)
        img_result = await imgQuery(city)

        header_img, header_img2, header_img3, base_img, food_img, architecture_img = img_result
        country, airport, dynamic_p1, dynamic_p2, dynamic_p3, dynamic_h1, dynamic_h2, dynamic_h3 = ai_result

        flightsearch = flightSearch(airport)
        c_price, c_fare, c_stops, c_layover, c_time, c_link = await fetch_flight_data(airport,
                                                                                      flightsearch.cheapest_search)
        a_price, a_fare, a_stops, a_layover, a_time, a_link = await fetch_flight_data(airport, flightsearch.average_search)

        e_price, e_fare, e_stops, e_layover, e_time, e_link = await fetch_flight_data(airport,flightsearch.expensive_search)

    return render_template("search.html", city=city, header_img=header_img, header_img2=header_img2,header_img3=header_img3, base_img=base_img, food_img=food_img,
                               architecture_img=architecture_img, country=country, dynamic_p1=dynamic_p1, dynamic_p2=dynamic_p2, dynamic_p3=dynamic_p3, dynamic_h1=dynamic_h1,
                                dynamic_h2=dynamic_h2, dynamic_h3=dynamic_h3, c_price=c_price, c_fare=c_fare,c_stops=c_stops,c_layover=c_layover,c_link=c_link, c_time=c_time,
                           a_price=a_price, a_fare=a_fare, a_stops=a_stops,a_layover=a_layover,a_time=a_time,a_link=a_link, e_price=e_price, e_fare=e_fare, e_stops=e_stops,
                           e_layover=e_layover,e_time=e_time,e_link=e_link)


@app.route("/test", methods=["GET", "POST"])
async def test():
    flightsearch = flightSearch("Tokyo")
    IATA = flightsearch.IATA()
    cheapest_flight_data = await flightsearch.cheapest_search(IATA)
    price = cheapest_flight_data[0]
    fare = cheapest_flight_data[1]
    stops = cheapest_flight_data[2]
    layover = cheapest_flight_data[3]
    time = cheapest_flight_data[4]
    link = cheapest_flight_data[5]
    print(time)
    return render_template("test.html")


@app.route("/edit-flight", methods=["GET", "POST"])
def edit_flight():
    return render_template("edit-flight.html")


# @app.route("/flight", methods=["GET", "POST"])
# async def flight():
#     if request.method == "POST":
#         city = request.form["flying-to"]
#         city_from =
#         ai_result = await aIQuery(city)
#         img_result = await imgQuery(city)
#         flightsearch = flightSearch(city)
#         IATA = flightsearch.IATA()
#         IATA_TO = flightsearch.IATA()
#
#         header_img, header_img2, header_img3, base_img, food_img, architecture_img = img_result
#         country, dynamic_p1, dynamic_p2, dynamic_p3, dynamic_h1, dynamic_h2, dynamic_h3 = ai_result
#
#     return render_template("search.html", city=city, header_img=header_img, header_img2=header_img2,header_img3=header_img3, base_img=base_img, food_img=food_img,
#                                architecture_img=architecture_img, country=country, dynamic_p1=dynamic_p1, dynamic_p2=dynamic_p2, dynamic_p3=dynamic_p3, dynamic_h1=dynamic_h1,
#                                 dynamic_h2=dynamic_h2, dynamic_h3=dynamic_h3)
if __name__ == "__main__":
    app.run(debug=True)


