from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from apscheduler.schedulers.background import BackgroundScheduler
from polygon import RESTClient


db = SQLAlchemy()
migrate = Migrate()
scheduler = BackgroundScheduler()
client = RESTClient('<add your token here>') 