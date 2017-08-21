"""
:created on: 2017-08-21

:author: Marcin Muszynski
:contact: marcinowski007@gmail.com
"""

from ..generic import GenericTestCase
from ..github_responses import PAGINATION_LINK_HEADER
from api.github_utils import GitHubUtils


class TestUtils(GenericTestCase):
    def test_pag_urls_extraction(self):
        """ Test for proper Link Header parsing """
        link = PAGINATION_LINK_HEADER
        expected = (
            'https://api.github.com/?page=1',
            'https://api.github.com/?page=1',
            'https://api.github.com/?page=3',
            'https://api.github.com/?page=119',
        )
        self.assertTupleEqual(GitHubUtils.extract_pagination_urls(link, 'https://api.github.com/'), expected)

    def test_incomplete_urls_extraction(self):
        """ In this test non existing keys are checked to be returned as None """
        link = ', '.join(PAGINATION_LINK_HEADER.split(', ')[:2])  # cutting off first & prev
        expected = (
            None,
            None,
            'https://api.github.com/?page=3',
            'https://api.github.com/?page=119',
        )
        self.assertTupleEqual(GitHubUtils.extract_pagination_urls(link, 'https://api.github.com/'), expected)
