from .user import PartialUser
from .errors import NoPossibleConversionException, LocaleNotFoundException


class Tag:
    """
    Defines a twitch stream tag
    """

    __slots__ = ('_id', '_auto_generated', '_localization_names', '_localization_descriptions')

    def __init__(self, data):
        self._id = data['tag_id']
        self._auto_generated = data['is_auto']
        self._localization_names = data['localization_names']
        self._localization_descriptions = data['localization_descriptions']

    def __eq__(self, other):
        if isinstance(other, PartialUser) or isinstance(other, Tag):
            return other.id == self._id
        elif isinstance(other, int):
            return other == self._id
        else:
            raise NoPossibleConversionException(f"Cannot compare type <{type(Tag)}> to <{type(other)}>")

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"<Tag - id:{self._id} auto_generated:{self._auto_generated} name(en-us):{self._localization_names['en-us']}>"

    def __str__(self):
        return self._localization_names['en-us']

    @property
    def id(self):
        return self._id

    @property
    def was_auto_generated(self):
        return self._auto_generated

    @property
    def localization_names_dict(self):
        return self._localization_names

    @property
    def localization_description_dict(self):
        return self._localization_descriptions

    @property
    def tag_data(self, locale='en-us'):
        if locale in self._localization_names and locale in self._localization_descriptions:
            return self._localization_names[locale], self._localization_descriptions[locale]
        else:
            raise LocaleNotFoundException(f"Locale '{locale}' not found in tag {self._id}")

    @property
    def tag_name(self, locale='en-us'):
        if locale in self._localization_names:
            return self._localization_names[locale]
        else:
            raise LocaleNotFoundException(f"Locale '{locale}' not found in tag {self._id}")

    @property
    def tag_description(self, locale='en-us'):
        if locale in self._localization_descriptions:
            return self._localization_descriptions[locale]
        else:
            raise LocaleNotFoundException(f"Locale '{locale}' not found in tag {self._id}")
