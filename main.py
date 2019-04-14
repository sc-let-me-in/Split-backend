import logging
import sys
import os

from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from household_routes import make_household_route
from user_routes import make_user_routes
from err import InvalidUsage
from models import Base

# setup logger
logging.basicConfig(stream=sys.stdout)
logger = logging.getLogger()

# setup db and conneciton
engine = create_engine(os.environ['DB_CONN'])
logger.debug("Database engine created")

DBSession = sessionmaker(bind=engine)
session = DBSession()
logger.debug("Database session bound to engine")

# create tables if they don't exist
Base.metadata.create_all(engine)
logger.debug("Tables created / exist")

app = Flask(__name__)
app.register_blueprint(make_user_routes(session))
app.register_blueprint(make_household_route(session))
app.secret_key = b'6hc/_gsh,./;2ZZx3c6_s,1//'


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/')
def hello_world():
    return 'Hello, World!'
