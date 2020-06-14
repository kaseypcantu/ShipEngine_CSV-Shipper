from dataclasses import dataclass, field
from typing import List, Optional


@dataclass(frozen=True)
class ShippingAddress:
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


@dataclass(frozen=True)
class PackageWeight:
    value: float
    unit: str

    def __post_init__(self):
        valid_units = ("pound", "ounce", "gram", "kilogram")
        if self.unit not in valid_units:
            raise ValueError(f"weight unit must be one of {valid_units}.")


@dataclass(frozen=True)
class PackageDimensions:
    unit: str
    length: float
    width: float
    height: float

    def __post_init__(self):
        valid_units = ("inch", "centimeter")
        if self.unit not in valid_units:
            raise ValueError(f"dimension unit must be one of {valid_units}.")


@dataclass(frozen=True)
class PackageInsuredValue:
    currency: str
    amount: float


@dataclass(frozen=True)
class PackageLabelMessages:
    reference1: str
    reference2: str
    reference3: str


@dataclass(frozen=True)
class Package:
    package_code: Optional[str]
    weight: PackageWeight
    dimensions: Optional[PackageDimensions]
    insured_value: Optional[PackageInsuredValue]
    label_messages: Optional[PackageLabelMessages]
    external_package_id: Optional[str]


@dataclass(frozen=True)
class CustomsItem:
    description: Optional[str]
    quantity: Optional[int]
    value: Optional[float]
    harmonized_tariff_code: Optional[str]
    country_of_origin: Optional[str]


@dataclass(frozen=True)
class CustomsOptions:
    contents: str
    non_delivery: str
    calculate_tax_amount: Optional[bool]
    preferred_currency: Optional[str]
    customs_items: List[CustomsItem]


@dataclass(frozen=True)
class User:
    """
    Represents someone who uses this integration. For now must be set up manually in the database.
    All fields come from ShipEngine API
    """

    token: str  # shipengine api key
    address: ShippingAddress
    length_unit: str
    weight_unit: str
    non_delivery: str


@dataclass(frozen=True)
class PrintRequest:
    """
    A PeopleVox print request
    """

    printRequestId: int
    printTemplateUrl: str
    status: str

    def __post_init__(self):
        valid_statuses = ("success", "not required", "fail")
        if self.status not in valid_statuses:
            raise ValueError(f"status must be one of {valid_statuses}")


@dataclass(frozen=True)
class TrackingNumber:
    trackingNumber: str
    trackingType: str

    def __post_init__(self):
        valid_types = ("outbound", "returns")

        if self.trackingType not in valid_types:
            raise ValueError(f"tracking_type must be one of {valid_types}")


@dataclass(frozen=True)
class Response:
    newPrintRequests: List[PrintRequest]
    trackingNumbers: List[TrackingNumber]
    status: str = None
    message: str = ""

    def __post_init__(self):
        if self.status is not None:
            valid_statuses = ("success", "partial", "fail")
            if self.status not in valid_statuses:
                raise ValueError(f"status must be one of {valid_statuses}")
            else:
                return

        failures = [pr.status == "fail" for pr in self.newPrintRequests]

        if all(failures):
            status = "fail"
        elif any(failures):
            status = "partial"
        else:
            status = "success"

        object.__setattr__(self, "status", status)
