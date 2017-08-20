"""
:created on: 2017-08-20

:author: Marcin Muszynski
:contact: marcinowski007@gmail.com
"""
import requests
from requests.auth import HTTPBasicAuth


class Github(object):
    API_URL = 'https://api.github.com'

    class BaseGithubException(Exception):
        """"""

    class GithubAuthException(BaseGithubException):
        """"""

    def __init__(self):
        self.authenticated = False

    def login(self, username, password, session=None):
        data = {'scopes': ['repo', 'user'], 'note': 'testing_purposes'}
        url = self.API_URL + '/authorizations'
        resp = requests.post(url, json=data, auth=HTTPBasicAuth(username, password))
        if resp.ok:
            return resp.json()['token']
        raise self.GithubAuthException

    def logout(self):
        self.authenticated = False

    def pull_request(self, **kwargs):
        if self.authenticated:
            pass
        pass

    def user(self, **kwargs):
        pass
