from .errors import NoPossibleConversionException


class PartialGame:
    """
    Defines a partial twitch game
    """
    __slots__ = ('_id')

    def __init__(self, _id):
        self._id = _id

    def __str__(self):
        return "None"

    def __repr__(self):
        return f"<PartialUser - id:{self._id}>"

    def __eq__(self, other):
        if isinstance(other, PartialGame) or isinstance(other, Game):
            return other.id == self._id
        elif isinstance(other, int):
            return other == int(self._id)
        elif isinstance(other, str):
            return other == self._id
        else:
            raise NoPossibleConversionException(f"Cannot compare type <{type(PartialGame)}> to <{type(other)}>")

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def id(self):
        return self._id

    async def fetch_game(self):
        # TODO:: return await core.get_game(self._id)
        pass


class Game:
    """
    Defines a twitch game
    """

    __slots__ = ('_id', '_name', '_box_art_url')

    def __init__(self, data):
        self._id = data['id']
        self._name = data['name']
        self._box_art_url = data['box_art_url']

    def __eq__(self, other):
        if isinstance(other, Game) or isinstance(other, PartialGame):
            return other.id == self._id
        elif isinstance(other, int):
            return other == int(self._id)
        elif isinstance(other, str):
            return other == self._id
        else:
            raise NoPossibleConversionException(f"Cannot compare type <{type(Game)}> to <{type(other)}>")

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"<Game - id:{self._id} name:{self._name} url:{self._box_art_url}>"

    def __str__(self):
        return self._name

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def box_art_url(self):
        return self._box_art_url
