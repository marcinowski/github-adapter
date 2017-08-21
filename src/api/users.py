"""
:created on: 2017-08-21

:author: Marcin Muszynski
:contact: marcinowski007@gmail.com
"""
import requests

from flask import session, request, Response
from flask_restplus import Namespace

from .generic import GitHubAdapterResource
from .decorators import catch_http_errors
from . import exceptions as ex

api = Namespace('user', description='User related operations')


@api.route('/')
class UserResource(GitHubAdapterResource):
    github_endpoint = '/users/{}/followers'

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
        url = self.GITHUB_API_URL + self.github_endpoint.format(username)
        pass

    def _get_followers(self, username):
        data = requests.get(self.github_ref.format(username) + '/followers')  # fixme: this response must be paginated
        urls = [v['url'] for v in data.json()]
        response = []
        for user_url in urls:
            d = requests.get(user_url)
            response.append(d.json())
        return response
