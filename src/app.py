"""
:created on: 2017-08-18

:author: Marcin Muszynski
:contact: marcinowski007@gmail.com
"""
from flask import Flask
from flask_restplus import Resource, Api

app = Flask(__name__)
api = Api(app)


@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

if __name__ == '__main__':
    app.run(debug=True)
