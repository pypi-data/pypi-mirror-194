from dataclasses import dataclass
from dataclass_wizard import JSONWizard


@dataclass
class TokensData(JSONWizard):
    access: str
    refresh: str
