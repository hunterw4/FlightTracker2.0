from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
from datetime import datetime, timedelta as td
from API import LocationSearch, openAi
from flight_API import expensiveSearch, flightSearch, customSearch
import asyncio
from aiohttp import ClientSession
import random

app = Flask(__name__)

Bootstrap5(app)

@app.route("/", methods=["GET", "POST"])
def home():
    videos = ["beach_bg", "beach_bg2", "beach_bg3"]
    random_video = random.randint(0, 2)
    video = videos[random_video]
    flights = ["Palermo", "Berlin", "Abu Dhabi"]
    cities = ["Paris", "Venice", "Tokyo", "Kyoto", "Rome", "Milan", "Florence"]
    country = ""
    flight_list = []
    poi_list = []
    for city in cities:
        locationsearch = LocationSearch(city, country)
        poi_img = locationsearch.base_img()
        poi_list.append((city, poi_img))
    for city in flights:
        locationsearch = LocationSearch(city,country)
        flight_img = locationsearch.base_img()
        flight_list.append((city, flight_img))
    return render_template("index.html", poi_list=poi_list, flight_list=flight_list, video=video)

    # if request.method == "POST":
    #     city = request.form["city"]
    #     locationsearch = LocationSearch(city)
    #     poi_img = locationsearch.base_img()
    #     poi_list = []
    #     poi_list.append((city, poi_img))
    #     return render_template("index.html", poi_list=poi_list)

# Current load time is 20 seconds

async def imgQuery(city, country):
    locationsearch = LocationSearch(city, country)
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


async def fetch_flight_data(city, airport, search_func):
    try:
        flightsearch = flightSearch(airport)
        flight = expensiveSearch(airport)
        IATA = flightsearch.IATA()
        data = await search_func(IATA)
        return (data[0], data[1], data[2], data[3], data[4], data[5])  # Return flight data as a tuple
    except TypeError:
        flightsearch = flightSearch(city)
        flight = expensiveSearch(city)
        IATA = flightsearch.IATA()
        data = await search_func(IATA)
        return (data[0], data[1], data[2], data[3], data[4], data[5])


async def fetch_custom_flight_data(airport, fly_from, flight_type, num_days, date, date_to, raw_fare, adults, children, search_func):
    fare = ""
    flight = customSearch(fly_from, airport)
    IATA = flight.IATA()
    IATA_TO = flight.IATA_TO()
    def get_fare(raw_fare):
        if raw_fare == "Economy class":
            fare = "M"
            return fare
        elif raw_fare == "Business class":
            fare = "C"
            return fare
        elif raw_fare == "First class":
            fare = "F"
            return fare
    get_fare(raw_fare)
    print(fare)
    data = await search_func(IATA, IATA_TO, flight_type, num_days, fare, date, date_to, adults, children)
    return (data[0], data[1], data[2], data[3], data[4], data[5])


# Current load time is 20 seconds
@app.route("/search", methods=["GET", "POST"])
async def search():
    if request.method == "POST":
        city = request.form["search"]
        ai_result = await aIQuery(city)
        country, airport, dynamic_p1, dynamic_p2, dynamic_p3, dynamic_h1, dynamic_h2, dynamic_h3 = ai_result
        img_result = await imgQuery(city, country)
        header_img, header_img2, header_img3, base_img, food_img, architecture_img = img_result

        f_type = "One-way"

        flightsearch = flightSearch(city)
        flight = expensiveSearch(city)
        c_price, c_fare, c_stops, c_layover, c_time, c_link = await fetch_flight_data(city, airport,
                                                                                      flightsearch.cheapest_search)
        a_price, a_fare, a_stops, a_layover, a_time, a_link = await fetch_flight_data(city,airport, flightsearch.average_search)

        e_price, e_fare, e_stops, e_layover, e_time, e_link = await fetch_flight_data(city, airport,flight.expensive_search)

    return render_template("search.html", city=city, header_img=header_img, header_img2=header_img2,header_img3=header_img3, base_img=base_img, food_img=food_img,
                               architecture_img=architecture_img, country=country, dynamic_p1=dynamic_p1, dynamic_p2=dynamic_p2, dynamic_p3=dynamic_p3, dynamic_h1=dynamic_h1,
                                dynamic_h2=dynamic_h2, dynamic_h3=dynamic_h3, c_price=c_price, c_fare=c_fare,c_stops=c_stops,c_layover=c_layover,c_link=c_link, c_time=c_time,
                           a_price=a_price, a_fare=a_fare, a_stops=a_stops,a_layover=a_layover,a_time=a_time,a_link=a_link, e_price=e_price, e_fare=e_fare, e_stops=e_stops,
                           e_layover=e_layover,e_time=e_time,e_link=e_link, f_type=f_type)


@app.route("/test", methods=["GET", "POST"])
async def test():
    city = request.form.get("boise")
    city_to = request.form.get("tokyo")
    raw_depart = "28/02/2024"
    raw_return = "05/03/2024"
    fare = "Economy"
    flight_type = "round"
    adults = 1
    children = 0


    flight = customSearch(city, city_to)

    IATA = flight.IATA()
    IATA_TO = flight.IATA_TO()

    test = await flight.average_custom(IATA,IATA_TO, flight_type, fare,raw_depart,raw_return,adults,children)
    print(test)





@app.route("/edit-flight", methods=["GET", "POST"])
def edit_flight():
    return render_template("edit-flight.html")


@app.route("/flight", methods=["GET", "POST"])
async def flight():
    if request.method == "POST":
        city = request.form.get("flying-from")
        city_to = request.form.get("flying-to")
        flight_type = request.form.get("flight-type")
        raw_depart = request.form.get("depart-date")
        raw_return = request.form.get("return-date")

        parsed_date = datetime.strptime(raw_depart, "%m/%d/%Y")
        # Convert the parsed date to the desired format
        date = parsed_date.strftime("%d/%m/%Y")
        parsed_return = datetime.strptime(raw_return, "%m/%d/%Y")
        date_to = parsed_return.strftime("%d/%m/%Y")

        difference = parsed_return - parsed_date

        # Get the number of days as an integer
        num_days = difference.days

        if flight_type == "round":
            f_type = "Round"
        else:
            f_type = "One-way"

        fare = request.form.get("class")
        adults = request.form.get("adults")
        children = request.form.get("children")
        ai_result = await aIQuery(city_to)
        img_result = await imgQuery(city_to)


        header_img, header_img2, header_img3, base_img, food_img, architecture_img = img_result
        country, airport, dynamic_p1, dynamic_p2, dynamic_p3, dynamic_h1, dynamic_h2, dynamic_h3 = ai_result

        flight = customSearch(city, airport)

        c_price, c_fare, c_stops, c_layover, c_time, c_link = await fetch_custom_flight_data(airport, city, flight_type, num_days,date, date_to,fare,adults,children,
                                                                                      flight.cheap_custom)
        a_price, a_fare, a_stops, a_layover, a_time, a_link = await fetch_custom_flight_data(airport, city, flight_type, num_days,date,date_to,fare,adults,children,
                                                                                      flight.average_custom)

        e_price, e_fare, e_stops, e_layover, e_time, e_link = await fetch_custom_flight_data(airport, city, flight_type, num_days,date,date_to,fare,adults,children,
                                                                                      flight.expensive_custom)

    return render_template("search.html", city=city_to, header_img=header_img, header_img2=header_img2,
                           header_img3=header_img3, base_img=base_img, food_img=food_img,
                           architecture_img=architecture_img, country=country, dynamic_p1=dynamic_p1,
                           dynamic_p2=dynamic_p2, dynamic_p3=dynamic_p3, dynamic_h1=dynamic_h1,
                           dynamic_h2=dynamic_h2, dynamic_h3=dynamic_h3, c_price=c_price, c_fare=c_fare,
                           c_stops=c_stops, c_layover=c_layover, c_link=c_link, c_time=c_time,
                           a_price=a_price, a_fare=a_fare, a_stops=a_stops, a_layover=a_layover, a_time=a_time,
                           a_link=a_link, e_price=e_price, e_fare=e_fare, e_stops=e_stops,
                           e_layover=e_layover, e_time=e_time, e_link=e_link, f_type=f_type)
if __name__ == "__main__":
    app.run(debug=True)


