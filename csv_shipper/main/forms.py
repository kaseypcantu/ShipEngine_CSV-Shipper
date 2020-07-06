from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.fields import TextAreaField
from wtforms.fields.html5 import EmailField, SearchField
from wtforms.validators import InputRequired, DataRequired, Length, Email


class ShippingAddressForm(FlaskForm):
    name = StringField(
        "Full Name", validators=[InputRequired(), DataRequired(), Length(min=2, max=25)]
    )
    phone = IntegerField(
        "Phone Number",
        validators=[InputRequired(), DataRequired(), Length(min=9, max=12)],
    )
    company_name = StringField("Company Name", validators=[Length(min=1, max=25)])
    address_line_1 = StringField(
        "Address Line 1",
        validators=[InputRequired(), DataRequired(), Length(min=2, max=60)],
    )
    address_line_2 = StringField("Address Line 2", validators=[Length(min=2, max=60)])
    address_line_3 = StringField("Address Line 3", validators=[Length(min=2, max=60)])
    city_locality = StringField(
        "City", validators=[InputRequired(), DataRequired(), Length(min=2, max=50)]
    )
    state_province = StringField(
        "State (2 character abbreviation)",
        validators=[InputRequired(), DataRequired(), Length(min=1, max=2)],
    )
    postal_code = StringField(
        "Postal Code",
        validators=[InputRequired(), DataRequired(), Length(min=1, max=15)],
    )
    country_code = StringField(
        "Country (2 character abbreviation)",
        validators=[InputRequired(), DataRequired(), Length(min=1, max=2)],
    )
    address_residential_indicator = SelectField(
        "Address Residential Indicator", choices=["unknown", "yes", "no"]
    )


class SchedulePickupForm(FlaskForm):
    label_id = StringField("Label ID", validators=[InputRequired(), DataRequired()])
    contact_name = StringField(
        "Full Name", validators=[InputRequired(), DataRequired()]
    )
    contact_email = EmailField(
        "Email", validators=[InputRequired(), DataRequired(), Email()]
    )
    contact_phone = StringField(
        "Phone Number", validators=[InputRequired(), DataRequired()]
    )
    pickup_notes = TextAreaField(
        "Pickup Notes", validators=[InputRequired(), DataRequired()]
    )
    schedule_pickup = SubmitField("Schedule Pickup")


class SearchBar(FlaskForm):
    search = SearchField()
