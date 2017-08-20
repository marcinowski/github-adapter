"""
:created on: 2017-08-21

:author: Marcin Muszynski
:contact: marcinowski007@gmail.com
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class PullRequestForm(FlaskForm):
    owner = StringField('Owner', validators=[DataRequired()], description='Owner of the repository')
    repo = StringField('Repository', validators=[DataRequired()], description='Repository name')
    title = StringField('PR Title', validators=[DataRequired()], description='Pull request title')
    head = StringField('Head', validators=[DataRequired()], description='Branch where changes were applied')
    base = StringField('Base', validators=[DataRequired()], description='Branch to merge the changes into')
    reviewers = StringField('Reviewers', description='Comma seperated list of revievers to assign')
    body = TextAreaField('PR body', description='Message to be attached to the pull request')


class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], description='Username of the user to fetch data')
