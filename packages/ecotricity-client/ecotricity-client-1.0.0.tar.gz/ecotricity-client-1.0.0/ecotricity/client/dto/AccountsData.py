from dataclasses import dataclass
from dataclass_wizard import JSONWizard

from ecotricity.client.dto import Account


@dataclass
class AccountsData(JSONWizard):
    results: list[Account]
