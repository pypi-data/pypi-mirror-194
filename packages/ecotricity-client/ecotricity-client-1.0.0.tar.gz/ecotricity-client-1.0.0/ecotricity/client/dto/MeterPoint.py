from dataclasses import dataclass
from dataclass_wizard import JSONWizard


@dataclass
class MeterPoint(JSONWizard):
    industry_id: str
    fuel_type: str
