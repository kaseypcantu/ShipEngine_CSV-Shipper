import os

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# from typing import Optional, List, Dict

load_dotenv()

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("POSTGRES_DB_URL")
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

db = SQLAlchemy(app)
db_session = db.session

from csv_shipper import routes
