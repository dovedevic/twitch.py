
class TwitchChannel:
    """
    The Base Twitch Channel Object
    """

    async def send(self, message):
        pass


class WhisperChannel(TwitchChannel):
    """
    The channel used to directly message a user
    """
    pass


class ChatChannel(TwitchChannel):
    """
    The channel used to message in a twitch channel chat
    """
    pass
