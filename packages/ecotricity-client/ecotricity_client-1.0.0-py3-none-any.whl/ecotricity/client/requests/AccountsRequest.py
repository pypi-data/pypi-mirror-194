import urllib.parse
from ecotricity.client.dto import AccountsResult, Session
from ecotricity.client.requests.BaseRequest import BaseRequest


class AccountsRequest(BaseRequest):
    path: str

    def __init__(self, host="api.ecotricity.co.uk", proto="https", path="/customers/v1/"):
        super().__init__(host, proto)
        self.path = path

    def get_accounts(self, session: Session) -> AccountsResult:
        variables = urllib.parse.quote(f'customers/{session.customer_id}/accounts')

        return self.read_data(self.path, variables, session, AccountsResult)
