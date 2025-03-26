from flask_app import app
from flask import render_template, redirect, url_for
#=-=-=-=--=#
#=-=-=-=-=-#
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
    # Will eventually have to interact with a DB to get POI's / User info.
    videos = ["beach_bg", "beach_bg2", "beach_bg3", "beach_bg4", "beach_bg5", "beach_bg6"]
    random_video = random.randint(0, 5)
    video = videos[random_video]
    flight_list = []
    poi_list = []
    return render_template("index.html", poi_list=poi_list, flight_list=flight_list, video=video)



# Current load time is 20 seconds
@app.route("/search/<location>", methods=["GET", "POST"])
def search(location):
    # Will need to validate the user input to certify that the city / country exists in the world csv
    return render_template('search.html')

@app.route("/edit-flight", methods=["GET", "POST"])
def edit_flight():
    # Will be one of the last things I do
    return render_template("edit-flight.html")






