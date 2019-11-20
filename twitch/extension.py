from .errors import APIMissMatchException, NoPossibleConversionException


class ExtensionType:
    """
    Defines the extension type twitch distinguishes
    """

    Component = 'component'
    Mobile = 'mobile'
    Panel = 'panel'
    Overlay = 'overlay'

    @staticmethod
    def ensure_type(etype):
        if etype == ExtensionType.Component or \
           etype == ExtensionType.Mobile or \
           etype == ExtensionType.Panel or \
           etype == ExtensionType.Overlay:
            return etype
        else:
            raise APIMissMatchException(f'ExtensionType<{etype}> is not valid!')


class Extension:
    """
    Defines a twitch extension
    """

    __slots__ = ('_id', '_version', '_name', '_activatable', '_type', '_position')

    def __init__(self, data):
        self._id = data['id']
        self._version = data['version']
        self._name = data['name']
        self._activatable = data['can_activate']
        self._type = []
        for etype in data['type']:
            self._type.append(ExtensionType.ensure_type(etype))
        self._position = (data['x'], data['y']) if 'x' in data and 'y' in data else None

    def __eq__(self, other):
        if isinstance(other, Extension):
            return other.id == self._id
        elif isinstance(other, str):
            return other == self._id
        else:
            raise NoPossibleConversionException(f"Cannot compare type <{type(Extension)}> to <{type(other)}>")

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"<Extension - {self._id} vers {self._version}>"

    def __str__(self):
        return f"Extension {self._id}: {self._name} v{self._version} has types [{', '.join(self._type)}]"

    @property
    def id(self):
        return self._id

    @property
    def version(self):
        return self._version

    @property
    def name(self):
        return self._name

    @property
    def activatable(self):
        return self._activatable

    @property
    def types(self):
        return self._type

    @property
    def is_component(self):
        return ExtensionType.Component in self._type

    @property
    def is_mobile(self):
        return ExtensionType.Mobile in self._type

    @property
    def is_panel(self):
        return ExtensionType.Panel in self._type

    @property
    def is_overlay(self):
        return ExtensionType.Overlay in self._type

    def position(self):
        return self._position
