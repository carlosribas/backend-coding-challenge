import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

# create application instance
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

# initializes extensions
db = SQLAlchemy(app)

from main.routes import *

if __name__ == '__main__':
    app.run()
