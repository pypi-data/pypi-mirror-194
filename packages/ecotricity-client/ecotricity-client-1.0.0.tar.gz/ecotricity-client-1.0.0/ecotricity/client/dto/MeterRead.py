from dataclasses import dataclass
from datetime import datetime
from dataclass_wizard import JSONWizard


@dataclass
class MeterRead(JSONWizard):
    id: str
    date: datetime
    created_at: datetime
    updated_at: datetime
    source: str
    value: float
    quality: str
    sequence_type: str
    register_industry_id: str
    meter_industry_id: str
    status: str
    submission_client: str
    account_id: str
    agreement_id: str
    meter_point_industry_id: str
