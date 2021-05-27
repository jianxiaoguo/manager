import json
import logging
import requests
from requests_toolbelt import user_agent
from api import __version__ as drycc_version

logger = logging.getLogger(__name__)


def get_session(access_token: str) -> requests.Session:
    session = requests.Session()
    session.headers = {
        'Content-Type': 'application/json',
        'User-Agent': user_agent('Drycc Manager ', drycc_version),
        'Authorization': 'token ' + access_token
    }
    return session


class WorkflowProxy(object):
    def __init__(self, access_token: str) -> None:
        self.session = get_session(access_token)

    def get(self, url: str, **kwargs) -> requests.Response:
        return self.session.get(url, params=kwargs)

    def post(self, url: str, **kwargs) -> requests.Response:
        return self.session.post(url, data=json.dumps(kwargs))

# def user_token(cluster: Cluster, username: str) -> str:
#     token = ''
#     try:
#         resp = requests.get(
#             url=cluster.ingress + '/v2/auth/tokens/{}/'.format(username),
#             headers={
#                 'Authorization': 'token {}'.format(admin_token(cluster)),
#                 'Content-Type': 'application/json',
#                 'User-Agent': user_agent('Drycc Manager ', drycc_version)
#             },
#             timeout=10)
#         if resp.status_code == 200 and resp.json().get('token'):
#             token = resp.json().get('token')
#             cache.set('drycc_controller_{}'.format(username), token)
#         elif resp.status_code == 403:
#             cache.delete('drycc_controller_{}'.format(cluster.admin))
#             user_token(cluster, username)
#         else:
#             logger.info(
#                 "have not obtain user's token, drycc response code {}".format(
#                     resp.status_code))  # noqa
#     except Exception as e:
#         logger.exception(e)
#     return token


# def admin_token(cluster: Cluster) -> str:
#     req_data = {
#         'username': cluster.admin,
#         'password': cluster.passwd
#     }
#     token = cache.get('drycc_controller_{}'.format(req_data['username']))
#     if token:
#         return token
#     try:
#         resp = requests.post(
#             url=cluster.ingress + '/v2/auth/login/',
#             data=req_data,
#             timeout=10)
#         if resp.status_code == 200 and resp.json().get('token'):
#             token = resp.json().get('token')
#             cache.set('drycc_controller_{}'.format(req_data['username']), token)
#     except Exception as e:
#         logger.exception(e)
#     return token
