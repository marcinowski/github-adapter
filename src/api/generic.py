"""
:created on: 2017-08-21

:author: Marcin Muszynski
:contact: marcinowski007@gmail.com
"""

import requests

from collections import OrderedDict
from flask import session, request
from flask_restplus import Resource
from requests.auth import HTTPBasicAuth
from urllib.parse import urlencode

from . import exceptions as ex
from .github_utils import GitHubUtils


class GitHubAdapterMixin(object):
    """
        This is a generic mixin class for all Resources used in GitHub Adapter API endpoints. It contains
        methods that are supposed to be used in public Resource "get/post" methods.

        :var GITHUB_API_URL: - it's a main Github API endpoint, shouldn't be overwritten
        :var github_endpoint: - path to use for specific query for this resource
        :var pagination_parameters: - available get params for this API endpoint at GitHub
        :var default_pagination_param: - pagination wouldn't show up if default params are not specified

        To build a proper resource URL:
            1. Combine self.GITHUB_API_URL and self.github_endpoint
            2. Format url above with some parts of path if necessary
            3. in case of GET request add GET params using self._get_build_params
        then you can `self.fetch_from_github` or `self.post_to_github` providing urls.
    """
    GITHUB_API_URL = 'https://api.github.com'

    github_endpoint = ''
    pagination_parameters = []
    query_parameters = []
    default_pagination_param = {}
    max_page_size = None

    def fetch_from_github(self, url, paginated=False):
        """
        Main method for fetching data from given resource. It's supposed to
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

    def post_to_github(self, url, data):
        """
        Main method for posting data to given resource. It's supposed to
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

    def build_get_params(self):
        """
        Main method for converting to GET Params
        :rtype: str
        """
        params = self._get_valid_params_from_request()
        return urlencode(params)

    def get_url(self, *args, **kwargs):
        """ Main method to be extended in child classes for getting url """
        raise NotImplementedError

    def is_authenticated(self):
        """ Checks if user is authenticated """
        if 'authenticated' in session:
            return session['authenticated']
        return False

    def _get_valid_params_from_request(self):
        """
        "Main" private method for building params for request
        :rtype: dict
        """
        params = self.default_pagination_param
        params.update(self._get_pagination_attrs_from_request())
        params.update(self._get_query_params_from_request())
        return params

    def _get_pagination_attrs_from_request(self):
        """ Private method for fetching pagination params from request. They must be attached to the url """
        pags = {k: v for k, v in request.args.items() if k in self.pagination_parameters}
        if pags.get('per_page', None) and self.max_page_size and int(pags['per_page']) > self.max_page_size:
            pags['per_page'] = self.max_page_size
        return pags

    def _get_query_params_from_request(self):
        """ Private method for fetching query params from request. They must be attached to the url """
        return {k: v for k, v in request.args.items() if k in self.query_parameters}

    @staticmethod
    def _requests_get(url, auth):
        """ Method excluded for easier testing """
        return requests.get(url, auth=auth)

    @staticmethod
    def _requests_post(url, data, auth):
        """ Method excluded for easier testing """
        return requests.post(url, json=data, auth=auth)

    def _get_session_auth(self):
        """ Extracts user credentials from flask session object """
        if self.is_authenticated():
            username, password = session.get('username'), session.get('password')
            return HTTPBasicAuth(username, password)
        return None

    @staticmethod
    def _handle_non_paginated_response(response):
        """ Simple non paginated response handling """
        data = response.json()
        return {'data': data}, response.status_code

    def _handle_paginated_response(self, response):
        """ Paginated response handling along with pagination info """
        data = response.json()
        urls = self._get_pagination_attributes(response)
        return self._format_rest_response(data, *urls), response.status_code

    def _get_pagination_attributes(self, response):
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
            return GitHubUtils.extract_pagination_urls(gh_pag, self.api.url_for(self))
        return (None, )*4

    @staticmethod
    def _handle_error_response(response):
        """
            Method that raises proper response error.
            Exception gets caught by decorator over main `get/post` function.
        """
        status_code = response.status_code
        reason = response.reason or ''
        exception = getattr(ex, ex.RESPONSE_EXCEPTION_NAME_FORMAT.format(status_code), ex.GitHubAdapter501Error)
        raise exception(reason)

    @staticmethod
    def _format_rest_response(data, first_url=None, next_url=None, previous_url=None, last_url=None):
        """ Formats data using unified template """
        template = OrderedDict([
            ('first_url', first_url),
            ('previous_url', previous_url),
            ('next_url', next_url),
            ('last_url', last_url),
            ('data', data)
        ])
        return template
