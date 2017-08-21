"""
:created on: 2017-08-18

:author: Marcin Muszynski
:contact: marcinowski007@gmail.com
"""

import pdb

import os
import requests

from flask import Flask, request, session, url_for, render_template, redirect

from src.settings import GITHUB_API_URL
from src.api import api
from src.api.auth import Auth
from src.forms import LoginForm, PullRequestForm, UserForm

app = Flask(__name__)


@app.route('/', methods=['GET'])
def main():
    return render_template('main.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return Auth().post()  # fixme: this can't be done this way
    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET'])
def logout():
    return render_template('main.html')


@app.route('/pull_request', methods=['GET', 'POST'])
def pull_request():
    form = PullRequestForm()
    if form.validate_on_submit():
        return ""
    return render_template('pull_request.html', form=form)


@app.route('/user', methods=['GET', 'POST'])
def user():
    form = UserForm()
    if form.validate_on_submit():
        return ""
    return render_template('user.html', form=form)


api.init_app(app)


if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run(debug=True)
