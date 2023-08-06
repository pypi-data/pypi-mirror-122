from vatis.live_asr.config_variables import API_KEY, AUTHENTICATION_PROVIDER_URL
import requests
from requests import Response


class ClientAuthorization:
    def __init__(self, auth_token: str, service_host: str):
        self._auth_token = auth_token
        self._service_host = service_host

    @property
    def auth_token(self) -> str:
        return self._auth_token

    @property
    def service_host(self) -> str:
        return self._service_host


def get_auth_token() -> ClientAuthorization:
    response: Response = requests.get(
        AUTHENTICATION_PROVIDER_URL,
        params={'service': 'LIVE_ASR'},
        headers={'Authorization': 'Bearer ' + API_KEY}
    )

    if response.status_code != 200:
        raise ConnectionAbortedError(f'Bad status code {response.status_code}')

    parsed = response.json()

    return ClientAuthorization(**parsed)

