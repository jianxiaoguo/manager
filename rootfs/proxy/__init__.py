import requests
import logging
from requests_toolbelt import user_agent
from django.core.cache import cache
from api import __version__ as drycc_version, models

logger = logging.getLogger(__name__)

session = None


def get_session(cluster_name, username):
    global session
    if session is None:
        token = cache.get('drycc_controller_{}'.format(username))
        if not token:
            token = user_token(cluster_name=cluster_name,
                               username=username)
        session = requests.Session()
        session.headers = {
            'Authorization': 'token ' + token,
            'Content-Type': 'application/json',
            'User-Agent': user_agent('Drycc Manager ', drycc_version)
        }
    return session


def user_token(cluster_name, username):
    token = None
    try:
        cluster = models.Clusters.objects.get(name=cluster_name)
    except models.Clusters.DoesNotExist:
        return None
    try:
        resp = requests.get(
            url=cluster.domain + '/v2/auth/tokens/{}/'.format(username),
            headers={
                'Authorization': 'token {}'.format(admin_token(cluster)),
                'Content-Type': 'application/json',
                'User-Agent': user_agent('Drycc Manager ', drycc_version)
            },
            timeout=10)
        if resp.status_code == 200 and resp.json().get('token'):
            token = resp.json().get('token')
            cache.set('drycc_controller_{}'.format(username), token)
        elif resp.status_code == 403:
            cache.delete('drycc_controller_{}'.format(cluster.admin))
            user_token(cluster_name, username)
        else:
            logger.info(
                "have not obtain user's token, drycc response code {}".format(
                    resp.status_code))  # noqa
    except Exception as e:
        logger.exception(e)
    return token


def admin_token(cluster):
    req_data = {
        'username': cluster.admin,
        'password': cluster.passwd
    }
    token = cache.get('drycc_controller_{}'.format(req_data['username']))
    if token:
        return token
    try:
        resp = requests.post(
            url=cluster.domain + '/v2/auth/login/',
            data=req_data,
            timeout=10)
        if resp.status_code == 200 and resp.json().get('token'):
            token = resp.json().get('token')
            cache.set('drycc_controller_{}'.format(req_data['username']), token)
    except Exception as e:
        logger.exception(e)
    return token
