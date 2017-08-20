"""
:created on: 2017-08-21

:author: Marcin Muszynski
:contact: marcinowski007@gmail.com
"""

from flask import session
from flask_restplus import Resource, Namespace


api = Namespace('auth', description='Authentication related operations')


@api.route('/login')
class Auth(Resource):
    def post(self):
        login = request.form['username']
        pwd = request.form['password']
        r = requests.get(GITHUB_API_URL + 'user', auth=HTTPBasicAuth(login, pwd))
        if r.ok:
            session['login'] = login
            session['authenticated'] = True
        return r.json(), r.status_code