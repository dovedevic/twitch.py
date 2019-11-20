from .errors import NoPossibleConversionException
from .genericutils import get_datetime_from


class Webhook:
    """
    Defines a twitch webhook
    """

    __slots__ = ('_topic', '_callback', '_expires_at')

    def __init__(self, data):
        self._topic = data['topic']
        self._callback = data['callback']
        self._expires_at = get_datetime_from(data['expires_at'])

    def __eq__(self, other):
        if isinstance(other, Webhook):
            return (other.topic == self._topic) and (other.callback == self._callback)
        else:
            raise NoPossibleConversionException(f"Cannot compare type <{type(Webhook)}> to <{type(other)}>")

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"<Webhook - topic:{self._topic} callback:{self._callback} exp_at:{self._expires_at}>"

    def __str__(self):
        return self._topic

    @property
    def topic(self):
        return self._topic

    @property
    def callback(self):
        return self._callback

    @property
    def expires_at(self):
        return self._expires_at
