"""
:created on: 2017-08-21

:author: Marcin Muszynski
:contact: marcinowski007@gmail.com
"""

import os
from unittest import TestCase

from app import app


class GenericTestCase(TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.app = app
        app.testing = True
        app.secret_key = os.urandom(24)

    def tearDown(self):
        app.testing = False
        app.secret_key = None
