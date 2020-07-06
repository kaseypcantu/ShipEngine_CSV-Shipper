from flask import render_template, flash, redirect, url_for, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from markupsafe import escape

from csv_shipper import bcrypt, db_session
from csv_shipper.models import User, db_add
from csv_shipper.users.utils import send_reset_email
from csv_shipper.users.forms import (
    SignUpForm,
    LoginForm,
    RequestResetForm,
    ResetPasswordForm,
)

users = Blueprint("users", __name__)


@users.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("users.dashboard"))
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        print(hashed_password)
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            username=form.username.data,
            pw_hash=hashed_password,
        )
        db_add(user)
        flash(
            f"Account created for {form.username.data}, you are now able to log in!",
            "primary",
        )
        return redirect(url_for("users.login"))
    return render_template("sign_up.html", title="Sign Up", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.username == form.username.data:
            if bcrypt.check_password_hash(user.pw_hash, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get("next")
                flash(f"Welcome {user.username}!", "primary")
                return (
                    redirect(next_page)
                    if next_page
                    else redirect(url_for("users.dashboard"))
                )
        else:
            flash(
                "Login Unsuccessful, please check your email and password and try again."
            )
    return render_template("log_in.html", title="Log In", form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))


@users.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    return render_template("dashboard.html", title="CSV_Shipper Dashboard")


@users.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("users.logout"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash(f"A password reset email has been sent to {form.email.data}", "info")
    return render_template("reset_request.html", title="Reset Password", form=form)


@users.route("/reset_password/<string:token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("users.logout"))
    user = User.verify_reset_token(token=token)
    if user is None:
        flash("That is an invalid or expired token.", "warning")
        return redirect(url_for("users.reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user.pw_hash = hashed_password
        db_session.commit()
        flash(
            f"Password updated for {form.username.data}, you are now able to log in!",
            "primary",
        )
        return redirect(url_for("users.login"))
    return render_template("reset_token.html", title="Reset Password", form=form)


@users.route("/user/<string:username>", methods=["GET"])
def show_user(username):
    user = User.query.filter_by(username=username).first_or_404(
        description=f"There is no data with the username: {escape(username)}"
    )
    return render_template("show_user.html", user=user)
