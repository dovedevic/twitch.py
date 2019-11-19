
class TwitchException(Exception):
    """
    Base exception class for twitch.py

    Any error thrown exclusively from this library should be able to be caught by this generic exception
    """
    pass


class APIMissMatchException(TwitchException):
    """
    Exception thrown when an argument from the API is received that does not match our API implementation

    If thrown, an issue and change must be made
    """
    pass


class NotAuthorizedError(TwitchException):
    """
    Exception thrown when an API call is made such that the client and token are not authorized to do

    If thrown, the user must be granted permission for said API call
    """
