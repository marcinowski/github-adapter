"""
:created on: 2017-08-21

:author: Marcin Muszynski
:contact: marcinowski007@gmail.com
"""

from flask import session
from flask_restplus import Resource, Namespace

from src.settings import GITHUB_API_URL

api = Namespace('user', description='User related operations')


@api.route('/')
class UserResource(Resource):
    github_ref = GITHUB_API_URL + 'users/'

    def get(self, username=None):
        """
        User data resource
        :param username:
        :return:
        """
        if session.get('authenticated', False):
            data = requests.get(self.github_ref.format(session['login']))
            return data.json(), 200
        else:
            username = request.args.get('username', None)
            if not username:
                return {}, 40

    def _get_followers(self, username):
        data = requests.get(self.github_ref.format(username) + '/followers')  # fixme: this response must be paginated
        urls = [v['url'] for v in data.json()]
        response = []
        for user_url in urls:
            d = requests.get(user_url)
            response.append(d.json())
        return response
