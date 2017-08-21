"""
:created on: 2017-08-21

:author: Marcin Muszynski
:contact: marcinowski007@gmail.com
"""
from flask import session, request
from flask_restplus import Namespace
from requests.auth import HTTPBasicAuth

from . import exceptions as ex
from .decorators import catch_http_errors
from .generic import GitHubAdapterResource

api = Namespace('auth', description='Authentication related operations')


@api.route('/login')
class AuthLogin(GitHubAdapterResource):
    """
    Resource for handling GitHub users authentication.
    """
    github_endpoint = '/user'

    @catch_http_errors
    def post(self):
        """
        Method for authenticating user. If authentication goes ok, credentials are added to sessions for later usage.
        HTTP POST data must contain
        :return: response data, status code
        :rtype: tuple
        """
        url = self._get_url()
        response, status_code = self._fetch_from_github(url)
        if status_code == 200:  # user authenticated
            if not self._is_authenticated():
                session['authenticated'] = True
                session['username'], session['password'] = self._get_credentials_from_request()
        else:
            raise ex.GitHubAdapter401Error('Wrong username and password combination.')
        return response, status_code

    def _get_url(self):
        return self.GITHUB_API_URL + self.github_endpoint

    def _get_session_auth(self):
        """ Overwriting to get credentials from authentication form """
        if self._is_authenticated():
            return super()._get_session_auth()
        return HTTPBasicAuth(*self._get_credentials_from_request())

    @staticmethod
    def _get_credentials_from_request():
        """ Fetches credentials from POST data """
        if 'username' not in request.form or 'password' not in request.form:
            raise ex.GitHubAdapter400Error('Missing parameters. Username and password are mandatory.')
        username = request.form['username']
        password = request.form['password']
        return username, password


@api.route('/logout')
class AuthLogout(GitHubAdapterResource):
    """ Simple class for removing auth data from session """
    @catch_http_errors
    def get(self):
        """
        Simple logging out mechanism, which removes user credentials from session.
        :return: response data, status code
        :rtype: tuple
        """
        if self._is_authenticated():
            session['authenticated'] = False
            session.pop('username', None)
            session.pop('password', None)
        return {'data': 'Logging out successful'}, 200

    def _get_url(self):
        """ Overwriting to implement all parent methods """
        return ''
