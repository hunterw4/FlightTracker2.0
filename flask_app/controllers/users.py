import os
from flask_app import app
from flask import render_template, redirect, url_for, request, abort, flash
#=-=-=-=--=#
import requests
from datetime import datetime, timedelta as td
#=-=-=-=-=-#
from API import LocationSearch, openAi
from flight_API import expensiveSearch, flightSearch, customSearch
#=-=-=-=--=#
import random
import datetime as dt


today = dt.date.today()



@app.route("/login", methods=["GET","POST"])
def login():
    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    return render_template("signup.html")


@app.route('/logout')
def logout():
    return redirect(url_for('home'))

@app.route("/", methods=["GET", "POST"])
def home():
    videos = ["beach_bg", "beach_bg2", "beach_bg3", "beach_bg4", "beach_bg5", "beach_bg6"]
    random_video = random.randint(0, 5)
    video = videos[random_video]
    flight_list = []
    poi_list = []
    return render_template("index.html", poi_list=poi_list, flight_list=flight_list, video=video)

# Current load time is 20 seconds

def imgQuery(city, country):
    pass

def aIQuery(city):
    pass


def fetch_flight_data(city, airport, search_func):
    pass


def fetch_custom_flight_data(airport, fly_from, flight_type, num_days, date, date_to, raw_fare, adults, children, search_func):
    pass


# Current load time is 20 seconds
@app.route("/search", methods=["GET", "POST"])
def search():
    return render_template('search.html')

@app.route("/edit-flight", methods=["GET", "POST"])
def edit_flight():
    return render_template("edit-flight.html")






