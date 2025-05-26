from flask_app import app
from flask_app.controllers import users, pois
from hypercorn.config import Config
from hypercorn.asyncio import serve
import asyncio

if __name__ == "__main__":
    config = Config()
    config.use_reloader = True
    asyncio.run(serve(app, config))