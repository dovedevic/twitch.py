from .user import PartialUser
from .errors import APIMissMatchException, NoPossibleConversionException


class SubscriptionType:
    """
    Defines the subscription tier twitch distinguishes
    """

    Tier1 = '1000'
    Tier2 = '2000'
    Tier3 = '3000'

    @staticmethod
    def ensure_type(stype):
        if stype == SubscriptionType.Tier1 or \
           stype == SubscriptionType.Tier2 or \
           stype == SubscriptionType.Tier3:
            return stype
        else:
            raise APIMissMatchException(f'TwitchBroadcasterType<{stype}> is not valid!')


class Subscription:
    """
    Defines a twitch subscription
    """

    __slots__ = ('_broadcaster', '_subscriber', '_is_gift', '_tier', '_name')

    def __init__(self, data):
        self._broadcaster = PartialUser(data['broadcaster_id'], data['broadcaster_name'])
        self._subscriber = PartialUser(data['user_id'], data['user_name'])
        self._is_gift = data['is_gift']
        self._tier = SubscriptionType.ensure_type(data['tier'])
        self._name = data['plan_name']

    def __eq__(self, other):
        if isinstance(other, Subscription):
            return self._broadcaster == other.broadcaster and self._subscriber == other.subscriber and self._tier == other.tier
        else:
            raise NoPossibleConversionException(f"Cannot compare type <{type(Subscription)}> to <{type(other)}>")

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"<Subscription - For {self._broadcaster} from {self._subscriber} of type {self._tier}:{self._is_gift}>"

    def __str__(self):
        return f"Tier {self._tier} Subscription: {self._subscriber} subbed to {self._broadcaster} via {'gift' if self._is_gift else 'purchase'}"

    @property
    def broadcaster(self):
        return self._broadcaster

    @property
    def subscriber(self):
        return self._subscriber

    @property
    def is_gift(self):
        return self._is_gift

    @property
    def tier(self):
        return self._tier

    @property
    def type(self):
        return self._tier

    @property
    def name(self):
        return self._name
