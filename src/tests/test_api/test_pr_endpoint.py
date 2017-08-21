"""
:created on: 2017-08-22

:author: Marcin Muszynski
:contact: marcinowski007@gmail.com
"""

from flask import session
from unittest.mock import MagicMock

from api.exceptions import GitHubAdapter400Error
from api.pull_request import PullRequestResource
from ..generic import GenericTestCase
from ..github_responses import PULL_REQUEST_RESPONSE, PULL_REQUEST_STATUS


class TestPullRequestResourceFunctional(GenericTestCase):
    """ Test class for main method testing """
    def test_main_flow(self):
        """ Owner supplied in data, all fields, should keep normal workflow """
        p = PullRequestResource()
        mock = MagicMock()
        mock.return_value = MockResponse()
        p._requests_post = mock
        data = {
            'owner': 'test_user',
            'repository': 'test_repository',
            'title': 'test_pull_request',
            'head': 'test_branch',
            'base': 'master',
            'reviewers': 'test_reviewer,test_reviewer_2',
            'body': 'This pull request is a test',
        }
        with self.app.test_request_context('/', data=data):
            resp, status = p.post()
        self.assertEqual(status, 201)

    def test_auth_main_flow(self):
        """ Owner supplied in session, all fields, should keep normal workflow """
        p = PullRequestResource()
        mock = MagicMock()
        mock.return_value = MockResponse()
        p._requests_post = mock
        data = {
            'repository': 'test_repository',
            'title': 'test_pull_request',
            'head': 'test_branch',
            'base': 'master',
            'reviewers': 'test_reviewer,test_reviewer_2',
            'body': 'This pull request is a test',
        }
        with self.app.test_request_context('/', data=data):
            session['authenticated'] = True
            session['username'] = 'test'
            resp, status_code = p.post()
        self.assertEqual(status_code, 201)


class TestPullRequestResourceUnit(GenericTestCase):
    """ Test class for testing PullRequestResource """
    def test_correct_data_validation(self):
        """ Owner supplied in data, all fields, should keep normal workflow """
        data = {
            'owner': 'test_user',
            'repository': 'test_repository',
            'title': 'test_pull_request',
            'head': 'test_branch',
            'base': 'master',
            'reviewers': 'test_reviewer,test_reviewer_2',
            'body': 'This pull request is a test',
        }
        with self.app.test_request_context('/', data=data):
            pr_data, rev = PullRequestResource()._validate_data()
        # nothing raised -> no need to check if data is fine
        self.assertEqual(rev, 'test_reviewer,test_reviewer_2')

    def test_incorrect_data_validation(self):
        """ Missing fields, should raise 400 """
        data = {
            'title': 'test_pull_request',
            'head': 'test_branch',
            'base': 'master',
            'reviewers': 'test_reviewer,test_reviewer_2',
            'body': 'This pull request is a test',
        }
        with self.app.test_request_context('/', data=data):
            with self.assertRaises(GitHubAdapter400Error):
                PullRequestResource()._validate_data()

    def test_correct_owner_from_session(self):
        """ If owner is not supplied then it should be fetched from session """
        data = {
            'repository': 'test',
            'title': 'test_pull_request',
            'head': 'test_branch',
            'base': 'master',
            'reviewers': 'test_reviewer,test_reviewer_2',
            'body': 'This pull request is a test',
        }
        with self.app.test_request_context('/', data=data):
            session['authenticated'] = True
            session['username'] = 'test'
            data, _ = PullRequestResource()._validate_data()
            self.assertEqual(data['owner'], 'test')

    def test_get_created_pr_url(self):
        """ Silly test for private method """
        u = PullRequestResource()._get_created_pr_url(PULL_REQUEST_RESPONSE)
        self.assertEqual(u, PULL_REQUEST_RESPONSE['url'])

    def test_revs_validation(self):
        """ Silly but this test saved the resource """
        with self.assertRaises(GitHubAdapter400Error):
            PullRequestResource()._validate_reviewers('test, test2')


class MockResponse(object):
    ok = True
    status_code = PULL_REQUEST_STATUS

    def __init__(self):
        self.data = PULL_REQUEST_RESPONSE

    def json(self):
        return self.data
