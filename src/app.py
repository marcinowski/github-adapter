"""
:created on: 2017-08-18

:author: Marcin Muszynski
:contact: marcinowski007@gmail.com
"""
import os
from flask import Flask, request, session
from flask_restplus import Resource, Api

app = Flask(__name__)
api = Api(app)


@app.route('/login', methods=['POST'])
def login():
    session['username'] = request.form['username']
    return redirect(url_for('index'))


@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run(debug=True)
