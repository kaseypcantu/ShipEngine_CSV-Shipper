import os
from dataclasses import dataclass

from dotenv import load_dotenv
from flask import Flask, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape
from sqlalchemy import func

# from typing import Optional, List, Dict
from forms import SignUpForm, LoginForm

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("POSTGRES_DB_URL")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

db = SQLAlchemy(app)
db_session = db.session


def db_add(obj):
    db_session.add(obj)
    return db_session.commit()


def db_rm(obj):
    db_session.remove(obj)
    return db_session.commit()


@dataclass
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    pw_hash = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(
            db.DateTime(timezone=True), default=func.now(), server_default=func.now()
    )

    # x = datetime.datetime.now()  |  x.strftime('- %a %b[%m]-%d-%Y @ %I:%M:%S %p -')

    #  [EXAMPLE]: usage of __init__(self) on a given class,
    #  not needed when using @dataclass decorator.
    # def __init__(self, first_name: str, last_name: str,
    #              email: str, username: str, pw_hash: str):
    #     self.first_name = first_name
    #     self.last_name = last_name
    #     self.email = email
    #     self.username = username
    #     self.pw_hash = pw_hash

    def __repr__(self):
        return f"<User {self.username}>"


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
    return render_template("log_in.html", title="Log In", form=form)


@app.route("/user/<string:username>", methods=["GET"])
def show_user(username):
    user = User.query.filter_by(username=username).first_or_404(
            description=f"There is no data with the username: {escape(username)}"
    )
    return render_template("show_user.html", user=user)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port="9999", debug=True)
