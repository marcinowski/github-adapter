"""
:created on: 2017-08-22

:author: Marcin Muszynski
:contact: marcinowski007@gmail.com
"""

from flask import session
from unittest.mock import MagicMock

from api.users import UserResource
from ..generic import GenericTestCase
from ..github_responses import USER_RESPONSE, USER_STATUS, ERROR_RESPONSE_401


class TestUserResourceFunctional(GenericTestCase):
    """
    Functional tests for UserResource.
    3 test cases:
        - user not authenticated - username in GET params
        - user authenticated - username in session
        - neither of above
    """
    def setUp(self):
        super().setUp()
        mock = MagicMock()
        mock.return_value = MockUserResponse()
        self.resource = UserResource()
        self.resource._requests_get = mock

    def test_nauth_user(self):
        with self.app.test_request_context('?username=test'):
            r, sc = self.resource.get()
        self.assertEqual(sc, 200)

    def test_auth_user(self):
        with self.app.test_request_context('?username=test'):
            session['authenticated'] = True
            session['username'] = 'test'
            r, sc = self.resource.get()
        self.assertEqual(sc, 200)

    def test_blank_username(self):
        with self.app.test_request_context('?error=test'):
            r, sc = self.resource.get()
            self.assertEqual(sc, 400)

    def test_error_response(self):
        self.resource._requests_get.return_value = MockUserErrorResponse()
        with self.app.test_request_context('?username=test'):
            r, sc = self.resource.get()
            self.assertEqual(sc, 401)


class MockUserResponse(object):
    ok = True
    status_code = USER_STATUS

    def __init__(self):
        self.data = USER_RESPONSE

    def json(self):
        return self.data


class MockUserErrorResponse(MockUserResponse):
    ok = False
    status_code = 401
    reason = ERROR_RESPONSE_401
