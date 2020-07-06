from flask import render_template, Blueprint

from csv_shipper import app, db_session

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return render_template("layout.html")


@main.route("/csv_shipper-webhook", methods=["POST"])
def consume_webhook():
    pass


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
