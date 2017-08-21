"""
:created on: 2017-08-21

:author: Marcin Muszynski
:contact: marcinowski007@gmail.com
"""

from . import exceptions as ex


def _get_flask_response(e):
    """
    Formats exception to Flask response (data, status_code) format.
    :param e: Exception class defined for GitHubAdapter
    :type e: ex.GitHubAdapterHTTPError
    :return: data, status_code
    :rtype: tuple
    """
    return {'status_code': e.status_code, 'reason': e.reason, 'detail_reason': str(e)}, e.status_code


def catch_http_errors(function):
    """
        Executes the function and in case of exception returns error description and appropriate HTTP status code.
        Return format is adjusted for Flask Response parsing (data, status_code).
     """
    def catcher(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except ex.GitHubAdapterHTTPError as e:
            return _get_flask_response(e)
    return catcher
