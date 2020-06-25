from flask import render_template, flash, redirect, url_for
from markupsafe import escape

from csv_shipper import app, db_session
from csv_shipper.models import User
from csv_shipper.forms import SignUpForm, LoginForm


@app.route("/")
def hello_world():
    return "Hello Python"


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}", "primary")
        return redirect(url_for("test_route"))
    return render_template("sign_up.html", title="Sign Up", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    # if form.validate_on_submit():
    return render_template("log_in.html", title="Log In", form=form)


@app.route("/user/<string:username>", methods=["GET"])
def show_user(username):
    user = User.query.filter_by(username=username).first_or_404(
            description=f"There is no data with the username: {escape(username)}"
    )
    return render_template("show_user.html", user=user)


@app.route("/csv_shipper-webhook", methods=["POST"])
def consume_webhook():
    pass


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
