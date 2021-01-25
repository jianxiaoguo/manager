import requests

from api.models import Cluster
from proxy import get_session


class WorkflowProxy(object):
    def __init__(self, cluster: Cluster, username: str):
        self.session = get_session(cluster, username)

    def get(self, url: str, **kwargs) -> requests.Response:
        return self.session.get(url, timeout=5, **kwargs)

