from dataclasses import dataclass


@dataclass
class Session:
    customer_id: str
    auth_token: str
