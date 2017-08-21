"""
:created on: 2017-08-21

:author: Marcin Muszynski
:contact: marcinowski007@gmail.com
"""

from . import exceptions as ex


def catch_http_errors(function):
    """ Executes the function and in case of exception """
    def catcher(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except ex.GitHubAdapterHTTPError as e:
            return e.reason, e.status_code
    return catcher
