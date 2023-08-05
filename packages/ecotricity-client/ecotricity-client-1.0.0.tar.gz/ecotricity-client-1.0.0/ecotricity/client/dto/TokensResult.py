from dataclasses import dataclass
from dataclass_wizard import JSONWizard

from . import TokensData


@dataclass
class TokensResult(JSONWizard):
    data: TokensData
    status: str
