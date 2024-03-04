import os

from flask import Flask, render_template, redirect, url_for, request, abort, flash
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from sqlalchemy.orm import relationship
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
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
import datetime as dt
from pathlib import Path


today = dt.date.today()

app = Flask(__name__)
app.config['SECRET_KEY'] = "8BYkEfBA6O6donzWlSihBXox7C0sKR6b"
# Specify the relative path to the SQLite database file
db_file_path = Path(__file__).parent / 'instance' / 'users.db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URL', f'sqlite:///{db_file_path}')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

Bootstrap5(app)



db = SQLAlchemy(app)

login_manager = LoginManager()

login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True)
    password = db.Column(db.String(250), nullable=False)
    createDate = db.Column(db.Integer, nullable=False)

    pois = db.relationship('POI', backref='user', lazy=True)

    flights = db.relationship('Flight', backref='user', lazy=True)


class POI(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(250), nullable=False)
    country = db.Column(db.String(250), nullable=False)
    img = db.Column(db.String(250), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Flight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(250), nullable=False)
    country = db.Column(db.String(250), nullable=False)
    img = db.Column(db.String(250), nullable=False)
    link = db.Column(db.String(250), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

with app.app_context():
    db.create_all()


@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("That email does not exist, please sign up!")
            return redirect(url_for("signup"))
        elif not check_password_hash(user.password, password):
            flash("Incorrect password please try again.")
            return redirect(url_for("login"))
        else:
            login_user(user)
            return redirect(url_for("home"))

    return render_template("login.html", logged_in=current_user.is_authenticated)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()
        if not user:
            if password == confirm_password:
                salted_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
                new_user = User(
                    name=name,
                    email=email,
                    password=salted_password,
                    createDate=today
                )
                db.session.add(new_user)
                db.session.commit()
                return render_template("login.html")
            else:
                return render_template("signup.html")
        else:
            flash("That email already exists in our database, please login")
            return redirect(url_for('login'))

    return render_template("signup.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/", methods=["GET", "POST"])
def home():
    videos = ["beach_bg", "beach_bg2", "beach_bg3", "beach_bg4", "beach_bg5", "beach_bg6"]
    random_video = random.randint(0, 5)
    video = videos[random_video]
    flight_list = []
    poi_list = []
    if current_user.is_authenticated:
        user_id = current_user.id
        user_pois = current_user.pois
        user_flights = current_user.flights
        for poi in user_pois:
            poi_info = {
                'city': poi.city,
                'country': poi.country,
                'img': poi.img
            }
            poi_list.append(poi_info)

            # Extract information for flights
        for flight in user_flights:
            flight_info = {
                'city': flight.city,
                'country': flight.country,
                'img': flight.img,
                'link': flight.link
            }
            flight_list.append(flight_info)
        return render_template("index.html", poi_list=poi_list, flight_list=flight_list, video=video,
                                   logged_in=current_user.is_authenticated)
    else:
        return render_template("index.html", poi_list=poi_list, flight_list=flight_list, video=video, logged_in=current_user.is_authenticated)

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
        if search_func == flight.expensive_search:
            IATA = flight.IATA()
            data = await search_func(IATA)
            return (data[0], data[1], data[2], data[3], data[4], data[5])
        else:
            IATA = flightsearch.IATA()
            data = await search_func(IATA)
            return (data[0], data[1], data[2], data[3], data[4], data[5])  # Return flight data as a tuple
    except TypeError:
        flightsearch = flightSearch(city)
        flight = expensiveSearch(city)
        if search_func == flight.expensive_search:
            IATA = flight.IATA()
            data = await search_func(IATA)
            return (data[0], data[1], data[2], data[3], data[4], data[5])
        else:
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
                           e_layover=e_layover,e_time=e_time,e_link=e_link, f_type=f_type, logged_in=current_user.is_authenticated)

@app.route("/edit-flight", methods=["GET", "POST"])
def edit_flight():
    return render_template("edit-flight.html", logged_in=current_user.is_authenticated)


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


        country, airport, dynamic_p1, dynamic_p2, dynamic_p3, dynamic_h1, dynamic_h2, dynamic_h3 = ai_result
        img_result = await imgQuery(city_to, country)
        header_img, header_img2, header_img3, base_img, food_img, architecture_img = img_result
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
                           e_layover=e_layover, e_time=e_time, e_link=e_link, f_type=f_type, logged_in=current_user.is_authenticated)

@app.route('/add_poi', methods=['POST'])
def add_poi_route():
    if request.method == "POST":
        city = request.form.get('city')
        country = request.form.get('country')
        img = request.form.get("base_img")
        user_id = current_user.id


        new_poi = POI(
            city=city,
            country=country,
            img=img,
            user_id=user_id,
        )
        db.session.add(new_poi)
        db.session.commit()
        return redirect(url_for('home'))



if __name__ == "__main__":
    app.run(debug=True)


