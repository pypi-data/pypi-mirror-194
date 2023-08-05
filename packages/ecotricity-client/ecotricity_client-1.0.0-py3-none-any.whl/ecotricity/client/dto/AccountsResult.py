from dataclasses import dataclass
from dataclass_wizard import JSONWizard

from . import AccountsData


@dataclass
class AccountsResult(JSONWizard):
    data: AccountsData
    status: str
