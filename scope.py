
class Scope:
    """
    Defines the scope string the documentation provides
    https://dev.twitch.tv/docs/authentication#scopes
    """

    class Analytics:
        """
        Defines the analytics scopes
        """

        class Games:
            """
            Defines the games scopes
            """
            _read = 'analytics:read:games'

            @classmethod
            def read(cls):
                return cls._read

        class Extensions:
            """
            Defines the extensions scopes
            """
            _read = 'analytics:read:extensions'

            @classmethod
            def read(cls):
                return cls._read

    class Bits:
        """
        Defines the bits scopes
        """
        _read = 'bits:read'

        @classmethod
        def read(cls):
            return cls._read

    class Channel:
        """
        Defines the channel scopes
        """
        _moderate = 'channel:moderate'

        @classmethod
        def moderate(cls):
            return cls._moderate

        class Subscriptions:
            """
            Defines the subscriptions scopes
            """
            _read = 'channel:read:subscriptions'

            @classmethod
            def read(cls):
                return cls._read

    class Chat:
        """
        Defines the chat scopes
        """
        _readonly = 'chat:read'
        _writeonly = 'chat:edit'

        @classmethod
        def readonly(cls):
            return cls._readonly

        @classmethod
        def writeonly(cls):
            return cls._writeonly

    class Whispers:
        """
        Defines the whispers scopes
        """
        _readonly = 'whispers:read'
        _sendonly = 'whispers:edit'

        @classmethod
        def readonly(cls):
            return cls._readonly

        @classmethod
        def sendonly(cls):
            return cls._sendonly

    class Clips:
        """
        Defines the clips scopes
        """
        _edit = 'clips:edit'

        @classmethod
        def edit(cls):
            return cls._edit

    class User:
        """
        Defines the user scopes
        """
        _manage = 'user:edit'

        @classmethod
        def manage(cls):
            return cls._manage

        class Email:
            """
            Defines the email scopes
            """
            _read = 'user:read:email'

            @classmethod
            def read(cls):
                return cls._read

        class Broadcast:
            """
            Defines the broadcast scopes
            """
            _readonly = 'user:read:broadcast'
            _readwrite = 'user:edit:broadcast'

            @classmethod
            def readonly(cls):
                return cls._readonly

            @classmethod
            def readwrite(cls):
                return cls._readwrite
