import os

from dotenv import load_dotenv
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

from csv_shipper.config import Config

# from typing import Optional, List, Dict

load_dotenv()

bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"
login_manager.session_protection = "strong"

mail = Mail()

db = SQLAlchemy()
db_session = db.session


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    app.app_context().push()

    db.init_app(app)

    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from csv_shipper.main.routes import main
    from csv_shipper.users.routes import users
    from csv_shipper.errors.handlers import errors

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(errors)

    return app
