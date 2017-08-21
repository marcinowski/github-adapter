"""
:created on: 2017-08-22

:author: Marcin Muszynski
:contact: marcinowski007@gmail.com
"""

from unittest.mock import MagicMock

from api.users import FollowersResource
from .test_users_endpoint import TestUserResourceFunctional, MockUserResponse, MockUserErrorResponse
from ..generic import GenericTestCase
from ..github_responses import FOLLOWERS_RESPONSE, FOLLOWERS_STATUS, ERROR_RESPONSE_401


class TestFollowersResourceFunctional(TestUserResourceFunctional):
    """ Functional tests are the same as in /user resource """
    def setUp(self):
        super().setUp()
        self.resource = FollowersResource()
        self.resource._requests_get = mock_resource_get

    def test_error_response(self):
        """ Different mocks require different assignments """
        self.resource._requests_get = mock_resource_error
        with self.app.test_request_context('?username=test'):
            r, sc = self.resource.get()
            self.assertEqual(sc, 401)


class TestFollowersResourceUnit(GenericTestCase):
    """ Unit tests for Followers Resource """
    def setUp(self):
        super().setUp()
        self.resource = FollowersResource()

    def test_get_error_followers_data(self):
        """ Error handling of response within single user data fetching """
        mock = MagicMock()
        mock.return_value = MockUserErrorResponse()
        self.resource._requests_get = mock
        with self.app.test_request_context('?username=test'):
            d = self.resource._single_follower_data('')
            self.assertTrue(isinstance(d, str))

    def test_get_ok_followers_data(self):
        """ Normal workflow for single user data fetching """
        mock = MagicMock()
        mock.return_value = MockUserResponse()
        self.resource._requests_get = mock
        with self.app.test_request_context('?username=test'):
            d = self.resource._single_follower_data('')
            self.assertTrue(isinstance(d, dict))
            self.assertListEqual(sorted(['name', 'email', 'public_repos', 'location']), sorted(list(d.keys())))


def mock_resource_error(url, *args):
    return MockFollowersErrorResponse()


def mock_resource_get(url, *args):
    if 'followers' in url:
        return MockFollowersResponse()
    return MockUserResponse()


class MockFollowersResponse(object):
    ok = True
    status_code = FOLLOWERS_STATUS
    headers = {'Link': ''}

    def __init__(self):
        self.data = FOLLOWERS_RESPONSE

    def json(self):
        return self.data


class MockFollowersErrorResponse(MockFollowersResponse):
    ok = False
    status_code = 401
    reason = ERROR_RESPONSE_401
