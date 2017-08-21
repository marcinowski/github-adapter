"""
:created on: 2017-08-21

:author: Marcin Muszynski
:contact: marcinowski007@gmail.com
"""
import requests

from requests.auth import HTTPBasicAuth
from flask import session
from flask_restplus import Resource

from . import exceptions as ex


class GitHubAdapterResource(Resource):
    GITHUB_API_URL = 'https://api.github.com'
    github_endpoint = ''

    def _get_github_response(self, url, paginated=False):
        """"""
        auth = self._get_session_auth()
        try:
            response = requests.get(url, auth=auth)
        except requests.RequestException:
            raise ex.GitHubAdapter500Error
        if not response.ok:
            return self._handle_error_response(response)
        if paginated:
            return self._handle_paginated_response(response)
        return self._handle_non_paginated_response(response)

    def _get_session_auth(self):
        if session.get('authenticated', None):
            username, password = session.get('username'), session.get('password')
            return HTTPBasicAuth(username, password)
        return None

    def _handle_paginated_response(self, response):
        pass

    def _handle_non_paginated_response(self, response):
        pass

    @staticmethod
    def _handle_error_response(response):
        """ Method that raises proper response error """
        status_code = response
        reason = response.reason or ''
        exception = getattr(ex, ex.RESPONSE_EXCEPTION_NAME_FORMAT.format(status_code), ex.GitHubAdapter501Error)
        raise exception(reason)
