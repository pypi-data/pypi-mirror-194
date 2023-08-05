from dataclasses import dataclass
from dataclass_wizard import JSONWizard


@dataclass
class BillingAddress(JSONWizard):
    postcode: str
    country_code: str
    address1: str = None
    address2: str = None
    address3: str = None
    address4: str = None
