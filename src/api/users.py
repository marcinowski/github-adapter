"""
:created on: 2017-08-21

:author: Marcin Muszynski
:contact: marcinowski007@gmail.com
"""

from flask import session, request, Response
from flask_restplus import Namespace

from . import exceptions as ex
from .generic import GitHubAdapterResource
from .decorators import catch_http_errors

api = Namespace('user', description='User related operations')


@api.route('/')
class UserResource(GitHubAdapterResource):
    github_endpoint = '/users/{}'
    query_parameters = ['username', ]

    @catch_http_errors
    def get(self):
        """
        User data resource. Returns all it's followers paginated (see documentation).
        Usage
            HTTP GET '../api/user?username=<username>'
            or if user is authenticated and wants to fetch his data:
            HTTP GET '../api/user'
        :return: List of users followers in json format
        :rtype: Response
        """
        if 'username' in request.args:
            username = request.args.get('username')
        elif session.get('authenticated', False):
            username = session.get('username')
        else:
            raise ex.GitHubAdapter400Error('Authenticate user or specify it by ?username=<username>')
        return self._get_data_for_user(username)

    def _get_data_for_user(self, username):
        url = self._get_url(username)
        rest_response = self._fetch_from_github(url)
        return rest_response

    def _get_url(self, username):
        return self.GITHUB_API_URL + self.github_endpoint.format(username)


@api.route('/followers')
class FollowersResource(UserResource):
    github_endpoint = '/users/{}/followers'
    pagination_parameters = ['page', 'per_page']
    default_pagination_param = {'per_page': 10}

    def _get_data_for_user(self, username):
        url = self.GITHUB_API_URL + self.github_endpoint.format(username) + '?' + self._build_get_params()
        followers, f_status_code = self._fetch_from_github(url, paginated=True)
        return followers, f_status_code

    def _get_pagination_attrs_from_request(self):
        """ This method is overwritten to enforce per_page=10, higher values are too heavy"""
        pags = super()._get_pagination_attrs_from_request()
        pags['per_page'] = 10
        return pags
