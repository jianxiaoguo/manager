import logging
import requests
from requests_toolbelt import user_agent
from django.core.cache import cache
from django.conf import settings
from api import __version__ as drycc_version
from api.models import Cluster

logger = logging.getLogger(__name__)


def get_session(cluster: Cluster, username: str,
                access_token: str) -> requests.Session:
    session = requests.Session()
    session.headers = {
        'Content-Type': 'application/json',
        'User-Agent': user_agent('drycc manager ', drycc_version)
    }
    if settings.LDAP_ENDPOINT:
        token = cache.get('drycc_controller_{}'.format(username))
        if not token:
            token = user_token(cluster=cluster,
                               username=username)
        session.headers['Authorization'] = 'token ' + token
    elif settings.OAUTH_ENABLE:
        session.headers['Authorization'] = 'token ' + access_token

    return session


def user_token(cluster: Cluster, username: str) -> str:
    token = ''
    try:
        resp = requests.get(
            url=cluster.ingress + '/v2/auth/tokens/{}/'.format(username),
            headers={
                'Authorization': 'token {}'.format(admin_token(cluster)),
                'Content-Type': 'application/json',
                'User-Agent': user_agent('drycc manager ', drycc_version)
            },
            timeout=10)
        if resp.status_code == 200 and resp.json().get('token'):
            token = resp.json().get('token')
            cache.set('drycc_controller_{}'.format(username), token)
        elif resp.status_code == 403:
            cache.delete('drycc_controller_{}'.format(cluster.admin))
            user_token(cluster, username)
        else:
            logger.info(
                "have not obtain user's token, drycc response code {}".format(
                    resp.status_code))  # noqa
    except Exception as e:
        logger.exception(e)
    return token


def admin_token(cluster: Cluster) -> str:
    req_data = {
        'username': cluster.admin,
        'password': cluster.passwd
    }
    token = cache.get('drycc_controller_{}'.format(req_data['username']))
    if token:
        return token
    try:
        resp = requests.post(
            url=cluster.ingress + '/v2/auth/login/',
            data=req_data,
            timeout=10)
        if resp.status_code == 200 and resp.json().get('token'):
            token = resp.json().get('token')
            cache.set('drycc_controller_{}'.format(req_data['username']), token)
    except Exception as e:
        logger.exception(e)
    return token


class WorkflowProxy(object):
    def __init__(self, cluster: Cluster, username: str,
                 access_token: str) -> None:
        self.session = get_session(cluster, username, access_token)

    def get(self, url: str, **kwargs) -> requests.Response:
        return self.session.get(url, params=kwargs)

    def post(self, url: str, **kwargs) -> requests.Response:
        return self.session.get(url, data=kwargs)
