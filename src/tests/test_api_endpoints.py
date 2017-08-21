"""
:created on: 2017-08-21

:author: Marcin Muszynski
:contact: marcinowski007@gmail.com
"""

from .generic import GenericTestCase
from api.generic import GitHubAdapterResource


class MockResource(GitHubAdapterResource):
    pagination_parameters = ['page', 'per_page']
    query_parameters = ['test', ]
    default_pagination_param = {'per_page': 10}


class TestGenericAPIResource(GenericTestCase):
    """ This class tests methods in GenericAPIResource """
    def test_build_params(self):
        with self.app.teestest


