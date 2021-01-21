from api.models import Cluster
from proxy import get_session


class WorkflowProxy(object):
    def __init__(self, cluster: Cluster, username: str):
        self.session = get_session(cluster, username)

    def get(self, url, **kwargs):
        return self.session.get(url, timeout=5, **kwargs)

