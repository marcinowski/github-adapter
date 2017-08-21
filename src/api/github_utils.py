"""
:created on: 2017-08-21

:author: Marcin Muszynski
:contact: marcinowski007@gmail.com
"""


class GitHubUtils(object):
    """ Class for various utilities for GitHub API operations """
    @classmethod
    def extract_pagination_urls(cls, link, path):
        """
        Example of a pagination link from headers is below.
        '<https://api.github.com/...?page=3>; rel="next", <https://api.github.com/...?page=119>; rel="last",
         <https://api.github.com/...?page=1>; rel="first", <https://api.github.com/...?page=1>; rel="prev"'
        This method gathers link from header, converts them to project API resource
        :param link: Content of 'Link' Header in GitHub paginated response
        :type link: str
        :param path:
        :type path: domain
        :return: first_link, previous_link, next_link, last_link in that order
        :rtype: tuple
        """
        pags = ['first', 'prev', 'next', 'last']
        urls = link.split(', ')
        urls_dict = {}
        for rel in urls:
            key, url = cls._handle_single_rel(rel, path)
            urls_dict[key] = url
        urls_tuple = tuple([urls_dict.get(pag, None) for pag in pags])
        return urls_tuple

    @classmethod
    def _handle_single_rel(cls, rel, path):
        raw_url, raw_key = rel.split('; ')
        url = cls._handle_raw_url(raw_url, path)
        key = cls._handle_raw_key(raw_key)
        return key, url

    @staticmethod
    def _handle_raw_url(raw_url, path):
        _url = raw_url.strip('<>')
        pags = _url.split('?')[-1]
        return '?'.join((path, pags))

    @staticmethod
    def _handle_raw_key(raw_key):
        _key = raw_key.lstrip('rel=')
        return _key.strip('"')
