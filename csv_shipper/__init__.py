import logging
import os

from devtools import PrettyFormat
from dotenv import load_dotenv
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

# from typing import Optional, List, Dict

load_dotenv()

app = Flask(__name__)

log: logging.Logger = app.logger
log.setLevel(logging.DEBUG)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("POSTGRES_DB_URL")
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

db = SQLAlchemy(app)
db_session = db.session

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"
login_manager.session_protection = "strong"

app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
app.config["MAIL_PORT"] = os.getenv("MAIL_PORT")
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USER")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PW")

mail = Mail(app)

prettier_python = PrettyFormat(
    indent_step=4,
    indent_char=".",
    repr_strings=True,
    simple_cutoff=2,
    width=120,
    yield_from_generators=False,  # default: True (whether to evaluate generators)
)

from csv_shipper.main.routes import main
from csv_shipper.users.routes import users

app.register_blueprint(main)
app.register_blueprint(users)
