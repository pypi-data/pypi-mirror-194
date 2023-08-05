from dataclasses import dataclass
from datetime import date
from dataclass_wizard import JSONWizard
from ecotricity.client.dto.Product import Product


@dataclass
class Agreement(JSONWizard):
    id: str
    display_number: str
    from_date: date
    fuel_type: str
    products: list[Product]
