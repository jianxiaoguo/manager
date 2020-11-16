from proxy import get_session


class DryccProxy(object):
    def __init__(self, cluster_name, username):
        self.session = get_session(cluster_name, username)

    def get(self, url, **kwargs):
        return self.session.get(url, **kwargs)

