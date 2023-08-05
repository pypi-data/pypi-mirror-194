from dataclasses import dataclass
from dataclass_wizard import JSONWizard

from . import MeterReadsData


@dataclass
class MeterReadsResult(JSONWizard):
    data: MeterReadsData
    status: str
