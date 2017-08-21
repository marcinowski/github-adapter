"""
:created on: 2017-08-21

:author: Marcin Muszynski
:contact: marcinowski007@gmail.com
"""
from unittest import TestCase, mock

from app import app


class GenericTestCase(TestCase):
    def setUp(self):
        self.client = app.test_client()
