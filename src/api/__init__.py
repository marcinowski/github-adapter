"""
:created on: 2017-08-19

:author: Marcin Muszynski
:contact: marcinowski007@gmail.com
"""
from flask_restplus import Api

from src.api.users import api as users
from src.api.pullrequest import api as pr
from src.api.auth import api as auth


api = Api(
    title='Github Adapter API',
    version='1.0',
    description='Contains API operations for fetching users data and pull request creation.',
    prefix='/api',
    doc='/api'
)

api.add_namespace(users)
api.add_namespace(pr)
api.add_namespace(auth)
