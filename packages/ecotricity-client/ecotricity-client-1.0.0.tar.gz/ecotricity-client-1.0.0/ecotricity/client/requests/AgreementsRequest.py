import urllib.parse
from ecotricity.client.dto import AgreementsResult, Session
from ecotricity.client.requests.BaseRequest import BaseRequest


class AgreementsRequest(BaseRequest):
    path: str

    def __init__(self, host="api.ecotricity.co.uk", proto="https", path="/customers/v1/"):
        super().__init__(host, proto)
        self.path = path

    def get_agreements(self, session: Session, account_id: str,) -> AgreementsResult:
        variables = urllib.parse.quote(f'customers/{session.customer_id}/accounts/{account_id}/agreements')

        return self.read_data(self.path, variables, session, AgreementsResult)
