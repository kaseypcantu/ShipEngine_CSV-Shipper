from dataclasses import dataclass
from enum import Enum, unique
from typing import List, Dict, Optional
from sqlalchemy import func

from csv_shipper import db, db_session


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
    token = db.Column(db.String(60), unique=True, nullable=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    pw_hash = db.Column(db.String(80), unique=True, nullable=False)
    ship_from_addresses = db.relationship("ShippingAddress",
                                          backref="users",
                                          lazy=True)
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
        return f"<User {self.username} {self.first_name} {self.last_name}>"


@dataclass
class ShippingAddress(db.Model):
    __tablename__ = "ship_from_addresses"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True, nullable=False)
    name = db.Column(db.String(50), unique=False, nullable=False)
    phone = db.Column(db.Integer, unique=False, nullable=False)
    company_name = db.Column(db.String(25), unique=False, nullable=True)
    address_line_1 = db.Column(db.String(60), unique=False, nullable=False)
    address_line_2 = db.Column(db.String(60), unique=False, nullable=True)
    address_line_3 = db.Column(db.String(60), unique=False, nullable=True)
    city_locality = db.Column(db.String(20), unique=False, nullable=False)
    state_province = db.Column(db.String(25), unique=False, nullable=False)
    postal_code = db.Column(db.Integer, unique=False, nullable=False)
    country_code = db.Column(db.String(2), unique=False, nullable=False)
    address_residential_indicator = db.Column(db.String(7), unique=False, nullable=False)

    def __post_init__(self):
        valid_residential_indicators = ("yes", "no", "unknown")
        if self.address_residential_indicator not in valid_residential_indicators:
            raise ValueError(f"address_residential_indicator must be on of {valid_residential_indicators}")


@dataclass
class Shipment:
    validate_address: Optional[str]
    external_order_id: Optional[str]


@dataclass
class RateOptions:
    carrier_ids: List[str]
    package_types: List[str]
    service_codes: List[str]
    calculate_tax_amount: bool
    preferred_currency: str

    def __post_init__(self):
        valid_currencies = ("usd", "cad", "aud", "gbp", "eur", "nzd")
        if self.preferred_currency not in valid_currencies:
            raise ValueError(f"preferred_currency must be one of {valid_currencies}")


@dataclass
class ShipToAddress:
    name: str
    phone: str
    company_name: Optional[str]
    address_line1: str
    address_line2: Optional[str]
    address_line3: Optional[str]
    city_locality: str
    state_province: str
    postal_code: str
    country_code: str
    address_residential_indicator: str

    def __post_init__(self):
        valid_residential_indicators = ("yes", "no", "unknown")
        if self.address_residential_indicator not in valid_residential_indicators:
            raise ValueError(f"address_residential_indicator must be on of {valid_residential_indicators}")


@unique
class SupportedCurrencies(Enum):
    usd = 1
    cad = 2
    aud = 3
    gbp = 4
    eur = 5
    nzd = 6

# @dataclass
# class Shipments(db.Model):
#     id = db.Column(db.Integer, primary_key=True,
#                    nullable=False,
#                    autoincrement=True)
#     shipment_id = db.Column(db.Integer, unique=True, nullable=False)
#     created_date = db.Column(db.DateTime(timezone=True),
#                              default=func.now(),
#                              server_default=func.now())


