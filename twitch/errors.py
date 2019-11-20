
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


class NotAuthorizedException(TwitchException):
    """
    Exception thrown when an API call is made such that the client and token are not authorized to do

    If thrown, the user must be granted permission for said API call
    """
    pass


class NoPossibleConversionException(TwitchException):
    """
    Exception thrown when a conversion or comparison is performed and no such defined conversion is defined

    If thrown, the user probably did something dumb
    """
    pass


class LocaleNotFoundException(TwitchException):
    """
    Exception thrown when a locale is requested for a tag or game but there does not exist one in the language

    If thrown, the user should pick a different locale
    """
    pass
