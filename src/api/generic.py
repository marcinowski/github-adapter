"""
:created on: 2017-08-21

:author: Marcin Muszynski
:contact: marcinowski007@gmail.com
"""

import requests

from collections import OrderedDict
from copy import deepcopy
from flask import session, request
from flask_restplus import Resource
from requests.auth import HTTPBasicAuth
from urllib.parse import urlencode

from . import exceptions as ex
from .github_utils import GitHubUtils


class GitHubAdapterResource(Resource):
    """
        This is a generic class for all Resources used in GitHub Adapter API endpoints. It contains
        private methods that are supposed to be used in main public "get/post" methods.
        Parameters:
            GITHUB_API_URL - it's a main Github API endpoint, shouldn't be overwritten
            github_endpoint - path to use for specific query for this resource
            pagination_parameters - available get params for this API endpoint at GitHub
            default_pagination_param - pagination wouldn't show up if default params are not specified
    """
    GITHUB_API_URL = 'https://api.github.com'
    github_endpoint = ''
    pagination_parameters = []
    default_pagination_param = {}

    def _fetch_from_github(self, url, paginated=False):
        """
        "Main" private method for fetching data from given resource. This is a private method, because it's supposed to
        be used under decorated "get" methods specified in routed Resources.
        This method handles GitHub response, authentication, pagination for HTTP GET request. It uses `requests` library
        underneath for HTTPBasicAuth and HTTP requests.
        :param url: full resource url
        :type url: str
        :param paginated: if response is expected to be paginated
        :type paginated: bool
        :return: formatted data, status_code
        :rtype: tuple
        :raises: ex.GitHubAdapterHTTPError
        """
        auth = self._get_session_auth()
        try:
            response = self._requests_get(url, auth)
        except requests.RequestException as e:
            raise ex.GitHubAdapter500Error(str(e))
        if not response.ok:
            return self._handle_error_response(response)
        if paginated:
            return self._handle_paginated_response(response)
        return self._handle_non_paginated_response(response)

    def _post_to_github(self, url, data):
        """
        "Main" private method for posting data to given resource. This is a private method, because it's supposed to
        be used under decorated "post" methods specified in routed Resources.
        This method handles GitHub response, authentication for HTTP POST request. It uses `requests` library
        underneath for HTTPBasicAuth and HTTP requests.
        Return data format is standarized with pagination, page_size, data and status_code.
        :param url: full resource url
        :type url: str
        :param data: data to be posted as a Python dict or list object convertible to `json`
        :type data: dict || list
        :return: formatted data, status_code
        :rtype: tuple
        :raises: ex.GitHubAdapterHTTPError
        """
        auth = self._get_session_auth()
        try:
            response = self._requests_post(url, data, auth)
        except requests.RequestException as e:
            raise ex.GitHubAdapter500Error(str(e))
        if not response.ok:
            return self._handle_error_response(response)
        return self._handle_non_paginated_response(response)

    def _get_pagination_attrs_from_request(self):
        """ Main method for fetching page_size, page etc. from request. They must be attached to the url """
        return {k: v for k, v in request.attrs.items() if k in self.pagination_parameters}

    def _define_get_params(self, **kwargs):
        """ Main method for converting to GET Params """
        query = deepcopy(self.default_pagination_param)
        query.update(kwargs)
        return urlencode(query)

    @staticmethod
    def _requests_get(url, auth):
        """ Method excluded for easier testing """
        return requests.get(url, auth=auth)

    @staticmethod
    def _requests_post(url, data, auth):
        """ Method excluded for easier testing """
        return requests.post(url, json=data, auth=auth)

    @staticmethod
    def _get_session_auth():
        """ Extracts user credentials from flask session object """
        if session.get('authenticated', None):
            username, password = session.get('username'), session.get('password')
            return HTTPBasicAuth(username, password)
        return None

    def _handle_non_paginated_response(self, response):
        """ Simple non paginated response handling """
        data = response.json()
        return self._format_rest_response(data), response.status_code

    def _handle_paginated_response(self, response):
        """ Paginated response handling along with pagination info """
        data = response.json()
        urls = self._get_pagination_attributes(response)
        return self._format_rest_response(data, *urls), response.status_code

    @staticmethod
    def _get_pagination_attributes(response):
        """
            This method extracts urls to
                - first_page
                - previous_page
                - next_page
                - last_page
            from the response and returns them in order as above.
        """
        gh_pag = response.headers.get('Link')
        if gh_pag:
            return GitHubUtils.extract_pagination_urls(gh_pag)
        return (None, )*4

    @staticmethod
    def _handle_error_response(response):
        """
            Method that raises proper response error.
            Exception gets caught by decorator over main `get/post` function.
        """
        status_code = response
        reason = response.reason or ''
        exception = getattr(ex, ex.RESPONSE_EXCEPTION_NAME_FORMAT.format(status_code), ex.GitHubAdapter501Error)
        raise exception(reason)

    @staticmethod
    def _format_rest_response(data, first_url=None, next_url=None, previous_url=None, last_url=None):
        template = OrderedDict([
            ('first_url', first_url),
            ('previous_url', previous_url),
            ('next_url', next_url),
            ('last_url', last_url),
            ('data', data)
        ])
        return template
