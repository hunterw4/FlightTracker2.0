from flask_app import app
from quart import render_template, redirect, url_for, request, session
#=-=-=-=--=#
#=-=-=-=-=-#
#=-=-=-=--=#
from flask_app.api.PhotoAPI import PhotoSearch
from flask_app.api.Ai_Response import Ai_Response
import asyncio
import random
import datetime as dt
import pandas as pd

location_data = pd.read_csv("flask_app/data/World.csv")
today = dt.date.today()


@app.route("/login")
async def login():
    return await render_template("login.html")


@app.route("/signup")
async def signup():
    return await render_template("signup.html")


@app.route('/logout')
async def logout():
    return await redirect(url_for('home'))


@app.route('/validate-search', methods=['POST'])
async def validate_search():
    form = await request.form
    city = form['location']
    if city in location_data['city'].values:
        return redirect(f'/search/{city}')
    else:
        return redirect('/')
    return await render_template('index.html')

@app.route("/", methods=["GET", "POST"])
async def home():
    session.clear()
    if 'user_responses' not in session:
        session['user_responses'] = []
    if 'ai_responses' not in session:
        session['ai_responses'] = []
    # Will eventually have to interact with a DB to get POI's / User info.
    videos = ["beach_bg", "beach_bg2", "beach_bg3", "beach_bg4", "beach_bg5"]
    random_video = random.randint(0, 4)
    video = videos[random_video]
    flight_list = []
    poi_list = []
    return await render_template("index.html", poi_list=poi_list, flight_list=flight_list, video=video)



@app.route("/search/<location>")
async def search(location):
    city_index = location_data.index[location_data['city'] == location].tolist()[0]
    country = location_data['country'][city_index]
    session['city'] = location
    # Initialize the classes
    photo = PhotoSearch(location, country)
    ai = Ai_Response(location)
    city_text = await ai.poi_response()
    food_text = await ai.food_response()
    architecture_text = await ai.architecture_response()
    city_header = await ai.poi_header()
    food_header = await ai.food_header()
    architecture_header = await ai.architecture_header()

    results = await photo.main()
    c_img, c_img2, c_img3, header_img, food_img, architecture_img = results
    return await render_template(
        "search.html",
        city=location,
        country=country,
        c_img=c_img,
        c_img2 = c_img2,
        c_img3 = c_img3,
        header_img=header_img,
        food_img=food_img,
        architecture_img=architecture_img,
        city_text = city_text,
        food_text = food_text,
        architecture_text = architecture_text,
        city_header = city_header,
        food_header = food_header,
        architecture_header = architecture_header
    )

@app.route("/edit-flight", methods=["GET", "POST"])
async def edit_flight():
    # Will be one of the last things I do
    return await render_template("edit-flight.html")






