from flask import render_template, Blueprint, current_app

from csv_shipper import db_session

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return render_template("layout.html")


@main.route("/csv_shipper-webhook", methods=["POST"])
def consume_webhook():
    pass
