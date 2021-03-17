import requests

from api.models import Cluster
from proxy import get_session


class WorkflowProxy(object):
    def __init__(self, cluster: Cluster, username: str, access_token: str) -> None:
        self.session = get_session(cluster, username, access_token)

    def get(self, url: str, **kwargs) -> requests.Response:
        return self.session.get(url, params=kwargs)

    def post(self, url: str, **kwargs) -> requests.Response:
        return self.session.get(url, data=kwargs)