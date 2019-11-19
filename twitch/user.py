from .errors import APIMissMatchException, NotAuthorizedException
from .channel import WhisperChannel


class TwitchBroadcasterType:
    """
    Defines the broadcasters twitch distinguishes
    """

    Partner = 'partner'  # The highest level of twitch designation
    Affiliate = 'affiliate'  # The middle level of twitch designation
    Broadcaster = ''  # The most basic level of twitch designation

    @staticmethod
    def ensure_type(btype):
        if btype == TwitchBroadcasterType.Partner or \
           btype == TwitchBroadcasterType.Affiliate or \
           btype == TwitchBroadcasterType.Broadcaster:
            return btype
        else:
            raise APIMissMatchException(f'TwitchBroadcasterType<{btype}> is not valid!')


class TwitchUserType:
    """
    Defines the user type twitch distinguishes
    """

    Staff = 'staff'  # The user is a member of twitch staff
    Admin = 'admin'  # The user is a twitch administrator
    GlobalMod = 'global_mod'  # The user is a twitch global moderator
    User = ''  # The user is a twitch user

    @staticmethod
    def ensure_type(utype):
        if utype == TwitchUserType.Staff or \
           utype == TwitchUserType.Admin or \
           utype == TwitchUserType.GlobalMod or \
           utype == TwitchUserType.User:
            return utype
        else:
            raise APIMissMatchException(f'TwitchUserType<{utype}> is not valid!')


class User(WhisperChannel):
    """
    Defines a twitch user
    """

    __slots__ = ('_broadcaster_type', '_description', '_displayname', '_email', '_id', '_username', '_offline_image_url', '_profile_image_url', '_user_type', '_view_count')

    def __init__(self, data):
        self._broadcaster_type = TwitchBroadcasterType.ensure_type(data['broadcaster_type'])
        self._user_type = TwitchUserType.ensure_type(data['type'])
        self._description = data['description']
        self._displayname = data['display_name']
        self._username = data['login']
        self._email = data['email'] if 'email' in data else ''
        self._id = data['id']
        self._profile_image_url = data['profile_image_url']
        self._offline_image_url = data['offline_image_url']
        self._view_count = data['view_count']

    @property
    def id(self):
        return self._id

    @property
    def username(self):
        return self._username

    @property
    def displayname(self):
        return self._displayname

    @property
    def description(self):
        return self._description

    @property
    def email(self):
        if self._email:
            return self._email
        else:
            raise NotAuthorizedError("You are not authorized to view this user's email")

    @property
    def profile_url(self):
        return self._profile_image_url

    @property
    def offline_url(self):
        return self._offline_image_url

    @property
    def view_count(self):
        return self._view_count

    @property
    def broadcaster_type(self):
        return self._broadcaster_type

    @property
    def user_type(self):
        return self._user_type

    @property
    def is_affiliate(self):
        return self._broadcaster_type == TwitchBroadcasterType.Affiliate

    @property
    def is_partnered(self):
        return self._broadcaster_type == TwitchBroadcasterType.Partner

    @property
    def is_admin(self):
        return self._user_type == TwitchUserType.Admin

    @property
    def is_staff(self):
        return self._user_type == TwitchUserType.Staff

    @property
    def is_global_moderator(self):
        return self._user_type == TwitchUserType.GlobalMod
