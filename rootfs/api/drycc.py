import json
import logging
import requests
from requests_toolbelt import user_agent
from api import __version__ as drycc_version

logger = logging.getLogger(__name__)


class DryccClient(object):
    def __init__(self, access_token: str) -> None:
        self.session = self._get_session(access_token)

    @staticmethod
    def _get_session(access_token: str) -> requests.Session:
        session = requests.Session()
        session.headers = {
            'Content-Type': 'application/json',
            'User-Agent': user_agent('Drycc Manager ', drycc_version),
            'Authorization': 'Bearer ' + access_token
        }
        return session

    def get(self, url: str, **kwargs) -> requests.Response:
        return self.session.get(url, params=kwargs)

    def delete(self, url: str, **kwargs) -> requests.Response:
        return self.session.delete(url, params=kwargs)

    def post(self, url: str, **kwargs) -> requests.Response:
        return self.session.post(url, data=json.dumps(kwargs))
