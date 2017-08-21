"""
:created on: 2017-08-21

:author: Marcin Muszynski
:contact: marcinowski007@gmail.com
"""
from unittest.mock import patch
from .generics import GenericTestCase


class TestUIEndpoints(GenericTestCase):
    def test_main_page(self):
        """ This test tests if `/` endpoint (main page) returns status 200 """
        r = self.client.get('/')
        self.assertEqual(r.status_code, 200)

    def test_login(self):
        """ This test tests if HTTP POST `/login` redirects to API endpoint """
        data = {'username': 'test', 'password': 'pwd'}
        with patch.object('api.auth.Auth', 'post') as m:
            self.client.post('/login', data=data)
        self.assertTrue(m.called)

    def test_create_pull_request(self):
        data = {
                'owner': 'test_user',
                'name': 'test_repository',
                'title': 'test_pull_request',
                'head': 'test_branch',
                'base': 'master',
                'reviewers': ['test_reviewer', 'test_reviewer_2'],
                'body': 'This pull request is a test',
            }
        with patch.object('api.pull_request.PullRequestResource', 'post') as m:
            self.client.post('/pull_request', data=data)
        self.assertTrue(m.called)

    def test_get_user_data(self):
        with patch.object('api.users.UserResource', 'get') as m:
            self.client.get('/user')
        self.assertTrue(m.called)
