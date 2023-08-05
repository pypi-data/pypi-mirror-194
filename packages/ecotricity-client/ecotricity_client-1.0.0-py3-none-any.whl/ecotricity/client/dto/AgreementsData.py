from dataclasses import dataclass
from dataclass_wizard import JSONWizard
from . import Agreement


@dataclass
class AgreementsData(JSONWizard):
    results: list[Agreement]
