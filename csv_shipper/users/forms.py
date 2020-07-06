from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import (
    InputRequired,
    DataRequired,
    Length,
    Email,
    EqualTo,
    ValidationError,
)

from csv_shipper.models import User


class SignUpForm(FlaskForm):
    """
    A class to be used with flask-wtf and wtforms to generate a Sign-Up form
    for the application. This form will create a new user and grant them access
    to the user dashboard.

    :param
        FlaskForm: An instance of a FlaskForm from flask_wtf.

    :returns
        A wtforms "form" object that can be supplied to the positional arguments
        of the `jinja2 render_template` function
    """

    first_name = StringField(
        "First Name",
        validators=[InputRequired(), DataRequired(), Length(min=2, max=25)],
    )
    last_name = StringField(
        "Last Name", validators=[InputRequired(), DataRequired(), Length(min=2, max=25)]
    )
    email = EmailField("Email", validators=[InputRequired(), DataRequired(), Email()])
    username = StringField(
        "Username", validators=[InputRequired(), DataRequired(), Length(min=8, max=20)]
    )
    password = PasswordField(
        "Password", validators=[InputRequired(), DataRequired(), Length(min=8, max=20)]
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            InputRequired(),
            DataRequired(),
            Length(min=8, max=20),
            EqualTo("password"),
        ],
    )
    submit = SubmitField("Sign Up")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    "That email is taken. Please choose a different email and try again."
                )

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    "That username is taken. Please choose a different username and try again."
                )


class LoginForm(FlaskForm):
    """
    A class to be used with flask-wtf and wtforms to generate a Log In form
    so that returning users may access their user dashboard.

    :param
        FlaskForm: An instance of a FlaskForm from flask_wtf.

    :returns
        A wtforms "form" object that can be supplied to the positional arguments
        of the `jinja2 render_template` function
    """

    email = EmailField("Email", validators=[InputRequired(), DataRequired(), Email()])
    username = StringField(
        "Username", validators=[InputRequired(), DataRequired(), Length(min=8, max=20)]
    )
    password = PasswordField(
        "Password", validators=[InputRequired(), DataRequired(), Length(min=8, max=20)]
    )
    remember = BooleanField("Remember Me")
    login = SubmitField("Log In")


class RequestResetForm(FlaskForm):
    email = EmailField("Email", validators=[InputRequired(), DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user is None:
                raise ValidationError(
                    f"There is no account with the email {user}, you must register first."
                )


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        "Password", validators=[InputRequired(), DataRequired(), Length(min=8, max=20)]
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            InputRequired(),
            DataRequired(),
            Length(min=8, max=20),
            EqualTo("password"),
        ],
    )
    submit = SubmitField("Reset Password")
