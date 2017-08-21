"""
:created on: 2017-08-21

:author: Marcin Muszynski
:contact: marcinowski007@gmail.com
"""
from flask_restplus import Resource


class GitHubAdapterResource(Resource):
    GITHUB_API_URL = 'https://api.github.com'
    github_endpoint = ''

    def _handle_paginated_response(self):
        pass
