"""
:created on: 2017-08-21

:author: Marcin Muszynski
:contact: marcinowski007@gmail.com
"""

from flask import session
from flask_restplus import Resource, Namespace

from src.settings import GITHUB_API_URL

api = Namespace('pull_request', description='Pull requests creation operations')


@api.route('/')
class PullRequestResource(Resource):
    """
    Test
    """
    github_ref = GITHUB_API_URL + '/repos/{owner}/{repo}/pulls'

    def post(self):
        """
        Pull Request creation resource
        Method for creating the pull request on selected repo for a given branch and automatically assigning users to
        review it.
        This method requires the request data to contain:
            - owner - owner of the repository (unless user is authenticated)
            - name - name of the repository
            - title - title of the pull request
            - head - name of the branch to be merged where changes are implemented
            - base - name of the branch to be merged into
            - reviewers - list of reviewers logins
            - body (optional) - content of pull request message (default is provided)
        Example of data body:

            {
                'owner': 'test_user',
                'name': 'test_repository',
                'title': 'test_pull_request',
                'head': 'test_branch',
                'base': 'master',
                'reviewers': ['test_reviewer', 'test_reviewer_2'],
                'body': 'This pull request is a test',
            }
        """
        data = request.form
        # data processing
        # post data to github_ref
        # process data - extract id
        # post data {reviewers: [..]} to github_ref + '/{id}/requested_reviewers
        return {'test': 'test'}, 201
