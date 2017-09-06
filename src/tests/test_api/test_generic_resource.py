"""
:created on: 2017-08-21

:author: Marcin Muszynski
:contact: marcinowski007@gmail.com
"""

from flask import session

from ..generic import GenericTestCase
from api import exceptions as ex
from api.generic import GitHubAdapterMixin


class TestGenericAPIResource(GenericTestCase):
    """ This class tests methods in GenericAPIResource """
    def test_build_params(self):
        with self.app.test_request_context('/?test=test&page=1&wrong=true'):
            params = MockResource()._get_valid_params_from_request()
        self.assertDictEqual(params, {'test': 'test', 'page': '1', 'per_page': 10})  # int of str -> doesn't matter

    def test_authenticated_session(self):
        with self.app.test_request_context('/'):
            session['authenticated'] = True
            self.assertTrue(MockResource().is_authenticated())

    def test_not_authenticated_session(self):
        with self.app.test_request_context('/'):
            self.assertFalse(MockResource().is_authenticated())

    def test_fetch_from_github_ok_npag(self):
        """ This tests ok response, not paginated"""
        with self.app.test_request_context('/'):
            resp, status_code = MockResource().fetch_from_github('/')
            expected_resp = {
                "data": ''
            }
            self.assertEqual(status_code, MockResponse.status_code)
            self.assertDictEqual(resp, expected_resp)

    def test_fetch_from_github_ok_pag(self):
        """ This tests ok response, paginated"""
        with self.app.test_request_context('/'):
            resp, _ = MockResource().fetch_from_github('/', paginated=True)
            expected_resp = {
                "first_url": None,
                "previous_url": None,
                "next_url": None,
                "last_url": None,
                "data": ''
            }
            self.assertDictEqual(resp, expected_resp)

    def test_fetch_from_github_nok(self):
        """ This tests ok response, paginated"""
        with self.app.test_request_context('/'):
            with self.assertRaises(ex.GitHubAdapter400Error):
                resp, _ = MockResource().post_to_github('/', data=None)


class MockResponse(object):
    ok = True
    status_code = 200
    reason = ''
    headers = {}

    def __init__(self, data):
        self.data = data

    def json(self):
        return self.data


class MockErrorResponse(MockResponse):
    ok = False
    status_code = 400


class MockResource(GitHubAdapterMixin):
    pagination_parameters = ['page', 'per_page']
    query_parameters = ['test', ]
    default_pagination_param = {'per_page': 10}

    def get_url(self, *args, **kwargs):
        pass

    @staticmethod
    def _requests_get(url, auth):
        return MockResponse('')

    @staticmethod
    def _requests_post(url, data, auth):
        return MockErrorResponse('')
