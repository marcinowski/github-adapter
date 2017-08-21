"""
:created on: 2017-08-18

:author: Marcin Muszynski
:contact: marcinowski007@gmail.com
"""

import os

from flask import Flask, render_template, redirect

from api import api
from forms import LoginForm, PullRequestForm, UserForm

app = Flask(__name__)
api.init_app(app)


@app.route('/', methods=['GET'])
def main():
    return render_template('main.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/api/auth/login', code=307)  # todo: url_for redirection?
    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET'])
def logout():
    return redirect('/api/auth/logout')


@app.route('/pull_request', methods=['GET', 'POST'])
def pull_request():
    form = PullRequestForm()
    if form.validate_on_submit():
        return redirect('/api/pull_request', code=307)
    return render_template('pull_request.html', form=form)


@app.route('/user', methods=['GET', 'POST'])
def user():
    form = UserForm()
    if form.validate_on_submit():
        return redirect('/api/user')
    return render_template('user.html', form=form)


if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run(debug=True)
