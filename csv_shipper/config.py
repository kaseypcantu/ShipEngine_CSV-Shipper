import os

from csv_shipper import load_dotenv

load_dotenv()


class Config:
    TEMPLATES_AUTO_RELOAD = True
    JSONIFY_PRETTYPRINT_REGULAR = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv("POSTGRES_DB_URL")
    SQLALCHEMY_ECHO = True
    SECRET_KEY = os.getenv("SECRET_KEY")
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USER")
    MAIL_PASSWORD = os.getenv("MAIL_PW")
