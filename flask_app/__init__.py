from quart import Quart

from flask_app.config.mysqlconnection import MySQLConnection

app = Quart(__name__)
app.config['SECRET_KEY'] = "8BYkEfBA6O6donzWlSihBXox7C0sKR6b"

@app.before_serving
async def init_pool():
    db = MySQLConnection('flighttracker')
    await db.create_pool()
    app.db = db