import dataclasses
import datetime
import logging
import os
import pprint as p
import json
from typing import List

import requests
from dotenv import load_dotenv
from requests import HTTPError
from requests.auth import AuthBase

from csv_shipper.models import (
    ShippingAddress,
    ShipFromAddress,
    ShipToAddress,
    Package,
    PackageWeight,
    PackageDimensions,
    CustomsOptions,
    Shipment,
    AdvancedOptions
)

load_dotenv()

logging.basicConfig(level=logging.DEBUG)

dt = datetime.datetime.now()


class ShipEngineAuth(AuthBase):
    def __init__(self, api_key):
        self.api_key = api_key

    def __call__(self, request):
        request.headers["API-Key"] = self.api_key
        return request


class ShipEngine:
    _BASE_URL = "https://api.shipengine.com/v1/"
    _CURRENT_DATE = dt.strftime("%m/%d/%Y")

    def __init__(self, api_key: str = os.getenv("SHIPENGINE_API_KEY"),
                 carrier_id: str = os.getenv("UPS_CARRIER-ID")):
        self.api_key = api_key
        self.carrier_id = carrier_id
        self.session = requests.Session()

    def request(self, method: str, endpoint: str, *args, **kwargs):
        kwargs["auth"] = ShipEngineAuth(self.api_key)

        try:
            resp = self.session.request(
                    method, self._BASE_URL + endpoint.strip("/"), *args, **kwargs
            )
            resp.raise_for_status()
            # logging.debug(json.dumps(resp.json(), indent=4))  logs the response from SE
            return resp.json()
        except HTTPError as e:
            error_obj = [err["message"] for err in e.response.json()["errors"]]
            logging.debug(f"Request Failed: {resp.status_code} | e: {e}\n\n ERROR: {json.dumps(error_obj, indent=4)}\n")
            return e, error_obj
        # The below will run after testing the above
        # resp = self.session.request(
        #     method, self._BASE_URL + endpoint.strip("/"), *args, **kwargs
        # )
        # resp.raise_for_status()
        # return resp.json()

    def get(self, endpoint, *args, **kwargs):
        return self.request("GET", endpoint, *args, **kwargs)

    def post(self, endpoint, *args, **kwargs):
        return self.request("POST", endpoint, *args, **kwargs)

    def create_label(
            self,
            ship_to_address: ShipToAddress,
            ship_from_address: ShipFromAddress,
            packages: List[Package],
            customs: CustomsOptions = None,
            advanced_opt: AdvancedOptions = None
    ):

        shipment = Shipment(
                carrier_id=self.carrier_id,
                service_code="ups_next_day_air",
                validate_address="validate_and_clean",
                external_shipment_id=None,
                external_order_id=None,
                items=None,
                ship_date=self._CURRENT_DATE,
                ship_to=dataclasses.asdict(ship_to_address),
                ship_from=dataclasses.asdict(ship_from_address),
                warehouse_id=None,
                return_to=None,
                confirmation="delivery",
                customs=customs,
                advanced_options=advanced_opt,
                insurance_provider="none",
                packages=[dataclasses.asdict(package) for package in packages]
        )

        if advanced_opt is not None:
            shipment.advanced_options = dataclasses.asdict(advanced_opt)

        if customs is not None:
            shipment.customs = dataclasses.asdict(customs)

        request = {"shipment": dataclasses.asdict(shipment)}

        return self.post("labels", json=request)


user_ship_from = ShipFromAddress(
        name="Monkey D. Luffy",
        phone="1-654-987-3124",
        company_name="The Grand Line",
        address_line1="3800 N Lamar Blvd",
        address_line2="Ste 220",
        address_line3=None,
        city_locality="Austin",
        state_province="TX",
        postal_code="78756",
        country_code="US",
        address_residential_indicator="no"
)

curative_ship_to = ShipToAddress(
        name="Kasey Cantu",
        phone="1-789-456-1234",
        company_name="ShipEngine",
        address_line1="4009 Marathon Blvd",
        address_line2="Suite 100",
        address_line3=None,
        city_locality="Austin",
        state_province="TX",
        postal_code="78756",
        country_code="US",
        address_residential_indicator="no"
)

weight = PackageWeight(
        value=2.5,
        unit="pound"
)

dims = PackageDimensions(
        unit="inch",
        length=12.5,
        width=12.5,
        height=12.5
)

package_1 = Package(
        weight=dataclasses.asdict(weight),
        dimensions=dataclasses.asdict(dims)
)

# se = ShipEngine(api_key=os.getenv("SHIPENGINE_API_KEY"), carrier_id=os.getenv("UPS_CARRIER-ID"))

se = ShipEngine()

r = se.create_label(ship_to_address=curative_ship_to,
                    ship_from_address=user_ship_from,
                    packages=[package_1])

print(r["label_id"])
p.pprint(r)
# p.pprint(r)
