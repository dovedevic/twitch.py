from datetime import datetime
from .errors import APIMissMatchException, NoPossibleConversionException
from .user import PartialUser


class TwitchProductType:
    """
    Defines the type of product twitch distinguishes
    """

    BitsExtension = 'BITS_IN_EXTENSION'  # Currently the only product twitch transactions tracks

    @staticmethod
    def ensure_type(ttype):
        if ttype == TwitchProductType.BitsExtension:
            return ttype
        else:
            raise APIMissMatchException(f'TwitchProductType<{ttype}> is not valid!')


class TwitchCostType:
    """
    Defines the type of cost twitch distinguishes
    """

    Bits = 'bits'  # Currently the only cost twitch transactions tracks

    @staticmethod
    def ensure_type(ctype):
        if ctype == TwitchCostType.Bits:
            return ctype
        else:
            raise APIMissMatchException(f'TwitchCostType<{ctype}> is not valid!')


class Transaction:
    """
    Defines a twitch transaction
    """

    __slots__ = ('_id', '_timestamp', '_to_user', '_from_user', '_product_type', '_sku', '_cost_amount', '_cost_type', '_product_name', '_product_in_development')

    def __init__(self, data):
        self._id = data['id']
        self._timestamp = datetime.strptime(data['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ')
        self._to_user = PartialUser(data['broadcaster_id'], data['broadcaster_name'])
        self._from_user = PartialUser(data['user_id'], data['user_name'])
        self._product_type = TwitchProductType.ensure_type(data['product_type'])
        self._sku = data['product_data']['sku']
        self._cost_amount = data['product_data']['cost']['amount']
        self._cost_type = TwitchCostType.ensure_type(data['product_data']['cost']['type'])
        self._product_name = data['product_data']['displayName']
        self._product_in_development = data['product_data']['inDevelopment']

    def __eq__(self, other):
        if isinstance(other, Transaction):
            return other.id == self._id
        elif isinstance(other, int):
            return other == self._id
        else:
            raise NoPossibleConversionException(f"Cannot compare type <{type(Transaction)}> to <{type(other)}>")

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"<Transaction - id:{self._id} sku:{self._sku} timestamp:{str(self._timestamp)}>"

    def __str__(self):
        return f"Transaction {self._id}: {self._from_user} paid {self._cost_amount} {self._cost_type} for {self._product_name} to {self._to_user} at {self._timestamp} SKU: {self._sku}"

    @property
    def id(self):
        return self._id

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def receiving_user(self):
        return self._to_user

    @property
    def giving_user(self):
        return self._from_user

    @property
    def product_type(self):
        return self._product_type

    @property
    def product_in_development(self):
        return self._product_in_development

    @property
    def sku(self):
        return self._sku

    @property
    def cost_amount(self):
        return self._cost_amount

    @property
    def cost_currency(self):
        return self._cost_type

    @property
    def product_name(self):
        return self._product_name
