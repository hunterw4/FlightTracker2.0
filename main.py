from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import datetime
from API import LocationSearch, openAi

app = Flask(__name__)

Bootstrap5(app)

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        city = request.form["search"]
        locationsearch = LocationSearch(city)
        header_img = locationsearch.header_img()
        base_img = locationsearch.base_img()
        food_img = locationsearch.food_img()
        architecture_img = locationsearch.architecture_img()
        gpt = openAi(city)
        country = gpt.aiResponseCountry()
        dynamic_p1 = gpt.aiResponseP1()
        dynamic_p2 = gpt.aiResponseP2()
        dynamic_p3 = gpt.aiResponseP3()
        dynamic_h1 = gpt.aiResponseH1()
        dynamic_h2 = gpt.aiResponseH2()
        dynamic_h3 = gpt.aiResponseH3()
        return render_template("search.html", city=city, header_img=header_img, base_img=base_img, food_img=food_img,
                               architecture_img=architecture_img, country=country, dynamic_p1=dynamic_p1, dynamic_p2=dynamic_p2, dynamic_p3=dynamic_p3, dynamic_h1=dynamic_h1,
                               dynamic_h2=dynamic_h2, dynamic_h3=dynamic_h3)


# @app.route("/<location>", methods=["GET", "POST"])
# def location():
#     pass


if __name__ == "__main__":
    app.run(debug=True)
