"""
:created on: 2017-08-21

:author: Marcin Muszynski
:contact: marcinowski007@gmail.com
"""


RESPONSE_EXCEPTION_NAME_FORMAT = 'GitHubAdapter{}Error'


class GitHubAdapterBaseError(Exception):
    """ Base Exception for GitHub adapter"""


class GitHubAdapterHTTPError(GitHubAdapterBaseError):
    """ Base HTTP Error Exception"""
    status_code = 400
    reason = ''


class GitHubAdapter400Error(GitHubAdapterHTTPError):
    """ Exception to raise for Bad Request """
    status_code = 400
    reason = 'Bad Request'


class GitHubAdapter401Error(GitHubAdapterHTTPError):
    """ Exception to raise when authentication error """
    status_code = 401
    reason = 'Authentication error'


class GitHubAdapter403Error(GitHubAdapterHTTPError):
    """ Exception to raise when authentication error """
    status_code = 403
    reason = 'Access denied'


class GitHubAdapter404Error(GitHubAdapterHTTPError):
    """ Exception to raise when resource is not found """
    status_code = 404
    reason = 'Page not found'


class GitHubAdapter405Error(GitHubAdapterHTTPError):
    """ Exception to raise when method is not allowed """
    status_code = 405
    reason = 'Method not allowed'


class GitHubAdapter422Error(GitHubAdapterHTTPError):
    """ Exception to raise when method is not allowed """
    status_code = 422
    reason = 'Unprocessable Entity - invalid fields received'


class GitHubAdapter500Error(GitHubAdapterHTTPError):
    status_code = 500
    reason = 'Server Error'


class GitHubAdapter501Error(GitHubAdapterHTTPError):
    status_code = 501
    reason = 'Unrecognized Error'
