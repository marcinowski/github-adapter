"""
:created on: 2017-08-21

:author: Marcin Muszynski
:contact: marcinowski007@gmail.com
"""
from flask_restplus import Namespace, Resource, fields


api = Namespace('cats', description='Cats related operations')

api