"""
:created on: 2017-08-21

:author: Marcin Muszynski
:contact: marcinowski007@gmail.com
"""
from ..generic import GenericTestCase

from api.decorators import catch_http_errors, _get_flask_response
from api.exceptions import GitHubAdapterHTTPError


class Error(GitHubAdapterHTTPError):
    reason = 'Test'
    status_code = 200


class TestDecorator(GenericTestCase):
    @catch_http_errors
    def _test_decorator(self):
        raise Error('')

    def test_decorator(self):
        """ This method tests if decorator works with catching GitHubAdapterHTTPErrors """
        reason, status_code = self._test_decorator()
        expected_reason, expected_status_code = _get_flask_response(Error(''))
        self.assertDictEqual(reason, expected_reason)
        self.assertEqual(status_code, expected_status_code)

    @catch_http_errors
    def _test_decorator_detail(self):
        raise Error('Detail message')

    def test_decorator_detail(self):
        """ This method tests if detail message is displayed in response """
        reason, _ = self._test_decorator_detail()
        self.assertEqual(reason.get('detail_reason'), 'Detail message')
