"""
:created on: 2017-08-21

:author: Marcin Muszynski
:contact: marcinowski007@gmail.com
"""


import re


class GitHubUtils(object):
    """ Class for various utilities for GitHub API operations """
    @classmethod
    def extract_pagination_urls(cls, link):
        """
        Example of a pagination link from headers is below.
        '<https://api.github.com/...?page=3>; rel="next", <https://api.github.com/...?page=119>; rel="last",
         <https://api.github.com/...?page=1>; rel="first", <https://api.github.com/...?page=1>; rel="prev"'
        :param link: Content of 'Link' Header in GitHub paginated response
        :type link: str
        :return: first_link, previous_link, next_link, last_link in that order
        :rtype: tuple
        """
        pags = ['first', 'prev', 'next', 'last']
        urls = link.split(', ')
        urls_dict = {}
        for rel in urls:
            key, url = cls._handle_single_rel(rel)
            urls_dict[key] = url
        urls_tuple = tuple([urls_dict.get(pag, None) for pag in pags])
        return urls_tuple

    @classmethod
    def _handle_single_rel(cls, rel):
        raw_url, raw_key = rel.split('; ')
        url = cls._handle_raw_url(raw_url)
        key = cls._handle_raw_key(raw_key)
        return key, url

    @staticmethod
    def _handle_raw_url(raw_url):
        return raw_url.strip('<>')

    @staticmethod
    def _handle_raw_key(raw_key):
        _key = raw_key.lstrip('rel=')
        return _key.strip('"')
