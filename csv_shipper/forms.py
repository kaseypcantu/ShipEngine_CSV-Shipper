from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    IntegerField,
    SelectField
)
from wtforms.fields.html5 import EmailField, SearchField
from wtforms.validators import (
    InputRequired,
    DataRequired,
    Length,
    Email,
    EqualTo
)


class SignUpForm(FlaskForm):
    """
    A class to be used with flask-wtf and wtforms to generate a Sign-Up form
    for the application. This form will create a new user and grant them access
    to the user dashboard.

    :param
        FlaskForm: An instance of a FlaskForm from flask_wtf.

    :returns
        A wtforms 'form' object that can be supplied to the positional arguments
        of the `jinja2 render_template` function
    """
    first_name = StringField('FirstName',
                             validators=[InputRequired(),
                                         DataRequired(),
                                         Length(min=2, max=25)])
    last_name = StringField('LastName',
                            validators=[InputRequired(),
                                        DataRequired(),
                                        Length(min=2, max=25)])
    email = EmailField('Email',
                       validators=[InputRequired(),
                                   DataRequired(),
                                   Email()])
    username = StringField('Username',
                           validators=[InputRequired(),
                                       DataRequired(),
                                       Length(min=8, max=20)])
    password = PasswordField('Password',
                             validators=[InputRequired(),
                                         DataRequired(),
                                         Length(min=8, max=20)])
    confirm_password = PasswordField('Password',
                                     validators=[InputRequired(),
                                                 DataRequired(),
                                                 Length(min=8, max=20),
                                                 EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    """
    A class to be used with flask-wtf and wtforms to generate a Log In form
    so that returning users may access their user dashboard.

    :param
        FlaskForm: An instance of a FlaskForm from flask_wtf.

    :returns
        A wtforms 'form' object that can be supplied to the positional arguments
        of the `jinja2 render_template` function
    """
    email = EmailField('Email',
                       validators=[InputRequired(),
                                   DataRequired(),
                                   Email()])
    username = StringField('Username',
                           validators=[InputRequired(),
                                       DataRequired(),
                                       Length(min=8, max=20)])
    password = PasswordField('Password',
                             validators=[InputRequired(),
                                         DataRequired(),
                                         Length(min=8, max=20)])
    remember = BooleanField('Remember Me')
    login = SubmitField('Log In')


class ShippingAddressForm(FlaskForm):
    name = StringField('Full Name', validators=[InputRequired(),
                                                DataRequired(),
                                                Length(min=2, max=25)])
    phone = IntegerField('Phone Number',
                         validators=[InputRequired(),
                                     DataRequired(),
                                     Length(min=9, max=12)])
    company_name = StringField('Company Name',
                               validators=[Length(min=1, max=25)])
    address_line_1 = StringField('Address Line 1', validators=[InputRequired(),
                                                               DataRequired(),
                                                               Length(min=2, max=60)])
    address_line_2 = StringField('Address Line 2', validators=[Length(min=2, max=60)])
    address_line_3 = StringField('Address Line 3', validators=[Length(min=2, max=60)])
    city_locality = StringField('City', validators=[InputRequired(),
                                                    DataRequired(),
                                                    Length(min=2, max=50)])
    state_province = StringField('State', validators=[InputRequired(),
                                                      DataRequired(),
                                                      Length(min=1, max=2)])
    postal_code = StringField('Postal Code', validators=[InputRequired(),
                                                         DataRequired(),
                                                         Length(min=1, max=15)])
    country_code = StringField("Country", validators=[InputRequired(),
                                                      DataRequired(),
                                                      Length(min=1, max=2)])
    address_residential_indicator = SelectField('Address Residential Indicator',
                                                choices=["unknown", "yes", "no"])


class SearchBar(FlaskForm):
    search = SearchField()


# class Shipment(FlaskForm):
