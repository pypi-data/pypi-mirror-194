import datetime
from dataclasses import dataclass
from dataclass_wizard import JSONWizard

from ecotricity.client.dto.BillingAddress import BillingAddress


@dataclass
class Account(JSONWizard):
    id: str
    from_date: datetime.date
    balance: float
    display_number: str
    billing_method: str
    display_billing_address: BillingAddress
    payment_method: str
    account_class: str
    in_dunning: bool
