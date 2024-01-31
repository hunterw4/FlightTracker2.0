from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import datetime

app = Flask(__name__)

Bootstrap5(app)

@app.route("/", methods=["GET","POST"])
def home():
    return render_template("index.html")




@app.route("/search", methods=["GET", "POST"])
def search():
    return render_template("search.html")



@app.route("/<location>", methods=["GET", "POST"])
def location():
    pass


if __name__ == "__main__":
    app.run(debug=True)