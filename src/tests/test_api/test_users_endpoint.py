"""
:created on: 2017-08-22

:author: Marcin Muszynski
:contact: marcinowski007@gmail.com
"""

from flask import session
from unittest.mock import MagicMock

from api.users import UserResource, FollowersResource
from ..generic import GenericTestCase
from ..github_responses import USER_RESPONSE


class TestUserResourceUnit(GenericTestCase):
    """ Unit tests for UserResource"""


