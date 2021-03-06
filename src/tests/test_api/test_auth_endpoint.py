"""
:created on: 2017-08-22

:author: Marcin Muszynski
:contact: marcinowski007@gmail.com
"""

from flask import session
from unittest.mock import MagicMock

from api.auth import AuthLogin, AuthLogout
from ..generic import GenericTestCase
from ..github_responses import AUTH_RESPONSE, AUTH_STATUS, ERROR_RESPONSE_401


class TestAuthResource(GenericTestCase):
    def test_login(self):
        """ Simple workflow test for fetching credentials from request """
        with self.app.test_request_context('/', data={'username': 'test', 'password': 'test'}):
            username, password = AuthLogin()._get_credentials_from_request()
            self.assertEqual(username, 'test')

    def test_storing_credentials(self):
        """ Simple test for keeping credentials in session while authenticating """
        a = AuthLogin()
        mock = MagicMock()
        mock.return_value = AUTH_RESPONSE, AUTH_STATUS
        a.fetch_from_github = mock
        with self.app.test_request_context('/', data={'username': 't_username', 'password': 'test'}):
            a.post()
            self.assertTrue(a.is_authenticated())
            self.assertEqual(session['username'], 't_username')

    def test_nok_response(self):
        """ Error GitHub response handling """
        a = AuthLogin()
        mock = MagicMock()
        mock.return_value = ERROR_RESPONSE_401, 401
        a.fetch_from_github = mock
        resp, status_code = a.post()
        self.assertEqual(status_code, 401)

    def test_logout(self):
        """ Simple workflow test for logging out """
        a = AuthLogout()
        with self.app.test_request_context('/'):
            session['authenticated'] = True
            a.get()
            self.assertFalse(a.is_authenticated())
            self.assertFalse('username' in session)
