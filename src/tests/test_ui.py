"""
:created on: 2017-08-21

:author: Marcin Muszynski
:contact: marcinowski007@gmail.com
"""

from .generic import GenericTestCase


class TestUIEndpoints(GenericTestCase):
    """
    Tests below simply check if routing is ok. These tests are copy&paste, but not that many in number so generic
    approach is not needed. They only need to show if any endpoint fails.
    """
    def test_main_page(self):
        """ This test tests if `/` endpoint (main page) is routed and generated """
        r = self.client.get('/')
        self.assertEqual(r.status_code, 200)

    def test_login_page(self):
        """ This tests if page for `/login` is routed and generated """
        r = self.client.get('/login')
        self.assertEqual(r.status_code, 200)

    def test_logout_page(self):
        """ This tests if page for `/logout` is routed and generated """
        r = self.client.get('/logout')
        self.assertEqual(r.status_code, 302)  # this one is redirected straight to API

    def test_user_page(self):
        """ This tests if page for `/user` is routed and generated """
        r = self.client.get('/user')
        self.assertEqual(r.status_code, 200)

    def test_followers_page(self):
        """ This tests if page for `/follower` is routed and generated """
        r = self.client.get('/followers')
        self.assertEqual(r.status_code, 200)

    def test_pull_request_page(self):
        """ This tests if page for `/pull_request` is routed and generated """
        r = self.client.get('/pull_request')
        self.assertEqual(r.status_code, 200)
