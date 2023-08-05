import jwt

from ecotricity.client.dto import Session
from ecotricity.client.requests import TokensRequest


def open_session(username: str, password: str) -> Session:
    request = TokensRequest()
    result = request.get_tokens(username, password)
    auth_token = result.data.access
    claims = jwt.decode(auth_token, options={'verify_signature': False})
    customer_id = claims['data']['customerId']
    return Session(customer_id, auth_token)
