import json
from json import JSONDecodeError
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from ecotricity.client.dto import TokensResult
from ecotricity.client.exceptions import ApiException
from ecotricity.client.exceptions import EcotricityClientException
from ecotricity.client.exceptions import ResponseDecodeException
from ecotricity.client.requests.BaseRequest import BaseRequest


class TokensRequest(BaseRequest):
    path: str

    def __init__(self, host="api.ecotricity.co.uk", proto="https", path="/auth/v2/tokens"):
        super().__init__(host, proto)
        self.path = path

    def get_tokens(self, username: str, password: str) -> TokensResult:
        body = str(json.dumps({'username': username, 'password': password})).encode('utf-8')
        r = Request(f'{self.proto}://{self.host}{self.path}')

        try:
            return TokensResult.from_json(urlopen(r, data=body).read().decode())
        except HTTPError as ex:
            raise ApiException("Failed to read from the API") from ex
        except JSONDecodeError as ex:
            raise ResponseDecodeException("Unable to decode response") from ex
        except Exception as ex:
            raise EcotricityClientException("Error while getting readings") from ex
