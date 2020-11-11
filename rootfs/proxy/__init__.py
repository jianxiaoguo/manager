import requests
import logging
from requests_toolbelt import user_agent
from django.core.cache import cache
from api import __version__ as drycc_version

logger = logging.getLogger(__name__)

session = None


def get_session(username):
    global session
    if session is None:
        token = cache.get('drycc_controller_{}'.format(username))
        if not token:
            # todo drycc_domain
            token = user_token(drycc_domain='drycc.uae-cg.uucin.com',
                               username=username)
        session = requests.Session()
        session.headers = {
            'Authorization': 'token ' + token,
            'Content-Type': 'application/json',
            'User-Agent': user_agent('Drycc Manager ', drycc_version)
        }
    return session


def user_token(drycc_domain, username):
    token = None
    admin_name = ''
    try:
        resp = requests.get(
            url=drycc_domain+'/v2/auth/tokens/{}/'.format(username),
            headers={
                'Authorization': 'token {}'.format(admin_token(drycc_domain)),
                'Content-Type': 'application/json',
                'User-Agent': user_agent('Drycc Manager ', drycc_version)
            },
            timeout=10)
        if resp.status_code == 200:
            token = resp.json().get('token')
            if token:
                cache.set('drycc_controller_{}'.format(username),
                          token)
        elif resp.status_code == 403:
            # todo admin username
            cache.delete('drycc_controller_{}'.format(admin_name))
            user_token(drycc_domain, username)
        else:
            logger.info("have not obtain user's token, drycc response code {}".format(resp.status_code))  # noqa
    except Exception as e:
        logger.exception(e)
    return token


def admin_token(drycc_domain):
    token = None
    # todo username/password
    admin_name = ''
    req_data = {
        'username': admin_name,
        'password': ''
    }
    try:
        resp = requests.post(
            url=drycc_domain+'/v2/auth/login/',
            data=req_data,
            timeout=10)
        if resp.status_code == 200:
            token = resp.json().get('token')
            if token:
                cache.set('drycc_controller_{}'.format(req_data['username']),
                          token)
    except Exception as e:
        logger.exception(e)
    return token


