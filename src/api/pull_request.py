"""
:created on: 2017-08-21

:author: Marcin Muszynski
:contact: marcinowski007@gmail.com
"""

from flask import session, request
from flask_restplus import Namespace

from . import exceptions as ex
from .decorators import catch_http_errors
from .generic import GitHubAdapterResource


api = Namespace('pull_request', description='Pull requests creation operations')


@api.route('/')
class PullRequestResource(GitHubAdapterResource):
    """
    Resource for creating pull requests and assigning reviewers
    """
    github_endpoint = '/repos/{}/{}/pulls'
    mandatory_fields = ['repository', 'title', 'head', 'base', 'reviewers']  # owner also, but can be stored in session
    optional_fields = ['body', 'owner']

    @catch_http_errors
    def post(self):
        """
        Method for creating the pull request on selected repository for a given branch and automatically assigning users
        to review it.
        This method requires the request data to contain:
            - owner - owner of the repository (unless user is authenticated)
            - repository - name of the repository
            - title - title of the pull request
            - head - name of the branch to be merged where changes are implemented
            - base - name of the branch to be merged into
            - reviewers - comma separated string of reviewers logins
            - body (optional) - content of pull request message (default is provided)
        Example of data body:

            {
                'owner': 'test_user',
                'repository': 'test_repository',
                'title': 'test_pull_request',
                'head': 'test_branch',
                'base': 'master',
                'reviewers': 'test_reviewer,test_reviewer_2',
                'body': 'This pull request is a test',
            }
        """
        pr_data, reviewers = self._validate_data()
        url = self._get_url(pr_data['owner'], pr_data['repository'])
        response, _ = self._post_to_github(url, pr_data)
        resp, status_code = self._add_reviewers(response['data'], reviewers)
        return resp, status_code

    def _get_url(self, username, repo):
        return self.GITHUB_API_URL + self.github_endpoint.format(username, repo)

    def _validate_data(self):
        """
        Data from the POST request must contain mandatory fields, may contain optional fields.
        In addition authentication is checked if 'owner' field is not passed.
        :return: data for creating Pull Request, list of reviewers
        :rtype: tuple
        """
        for key in self.mandatory_fields:
            if key not in request.form:
                raise ex.GitHubAdapter400Error('{} missing from data'.format(key))
        data = self._copy_request_form()
        if 'owner' not in data:
            if not self._is_authenticated():
                raise ex.GitHubAdapter400Error('You must either provide owner of '
                                               'the repository in HTTP POST body or be authenticated')
            data['owner'] = session.get('username')
        reviewers = data.pop('reviewers')
        self._validate_reviewers(reviewers)
        return data, reviewers

    @staticmethod
    def _validate_reviewers(revs):
        """ Reviewers should not contain spaces """
        if ' ' in revs:
            raise ex.GitHubAdapter400Error("Reviewers should be ','"
                                           " comma separated only without spaces i.e. 'login1,login2'")

    def _copy_request_form(self):
        """ Copies request.form with only necessary keys """
        return {k: v for k, v in request.form.items() if k in self.mandatory_fields + self.optional_fields}

    def _add_reviewers(self, pr_data, reviewers):
        """ Simply posts list of reviewers to new endpoint """
        url = self._get_created_pr_url(pr_data) + '/requested_reviewers'
        rev_list = reviewers.split(',')
        return self._post_to_github(url, rev_list)

    @staticmethod
    def _get_created_pr_url(pr_data):
        """
        Gets url from newly created Pull Request
        :return: url
        :rtype: str
        :raises: ex.GitHubAdapterHTTPError
        """
        try:
            return pr_data.get('url')
        except KeyError:
            raise ex.GitHubAdapter501Error('Oops. Something went wrong with Pull Request Creation')
