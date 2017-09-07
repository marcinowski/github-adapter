"""
:created on: 2017-08-21

:author: Marcin Muszynski
:contact: marcinowski007@gmail.com
"""

from collections import OrderedDict
from flask import session, request, Response
from flask_restplus import Namespace, Resource

from . import exceptions as ex
from .generic import GitHubAdapterMixin, AsyncGitHubAdapterMixin
from .decorators import catch_http_errors

api = Namespace('user', description='User related operations')


@api.route('/')
class UserResource(Resource, GitHubAdapterMixin):
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
        elif self.is_authenticated():
            username = session.get('username')
        else:
            raise ex.GitHubAdapter400Error('Authenticate user or specify it by ?username=<username>')
        return self._get_data_for_user(username)

    def get_url(self, username):
        """ Build url for user endpoint in GitHub """
        return self.GITHUB_API_URL + self.github_endpoint.format(username)

    def _get_data_for_user(self, username):
        """ Fetches data for specified username """
        url = self.get_url(username)
        rest_response = self.fetch_from_github(url)
        return rest_response


@api.route('/followers')
class FollowersResource(UserResource, AsyncGitHubAdapterMixin):
    """ Note! This class inherits after UserResource, since the `get` method implementations are the same. """
    github_endpoint = '/users/{}/followers'
    pagination_parameters = ['page', 'per_page']
    max_page_size = 50
    default_pagination_param = {'per_page': 5}

    def _get_data_for_user(self, username):
        """ Gathers data for all followers of selected user """
        url = self.get_url(username)
        followers_resp, f_status_code = self.fetch_from_github(url, paginated=True)
        return self._get_followers_data(followers_resp), f_status_code

    def get_url(self, username):
        """ BUild url for followers endpoint on GitHub """
        return self.GITHUB_API_URL + self.github_endpoint.format(username) + '?' + self.build_get_params()

    def _get_followers_data(self, followers):
        """
        Gets data for all followers and returns it.
        Note! Followers are passed as a mutable but it's an OrderedDict, so we want to keep the order.
        :param followers: rest response dictionary as formatted by GitHub adapter
        :type followers: OrderedDict
        :return: fetched and formatted data
        :rtype: OrderedDict
        """
        old_data = followers.pop('data')
        urls = [k.get('url', '') for k in old_data]
        data = self.fetch_many_from_github(urls)
        parsed_data = self._parse_followers_data(data)
        followers['data'] = parsed_data
        return followers

    def _parse_followers_data(self, data):
        """ Fetching and parsing single follower """
        p_data = []
        for resp, status in data:
            if status > 400:
                p_data.append("{} HTTP error for fetching data. Reason {}.".format(status, resp))
            else:
                p_data.append(self._parse_single_follower_data(resp))
        return p_data

    @staticmethod
    def _parse_single_follower_data(data):
        """ Cutting off not necessary keys, as indicated by specification """
        expected_keys = ['name', 'location', 'email', 'public_repos', 'login']
        return {k: v for k, v in data.items() if k in expected_keys}
