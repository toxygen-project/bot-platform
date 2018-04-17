import core.util as util


class PermissionChecker(util.ToxSave):

    DEFAULT_ROLES = ['user']

    def __init__(self, settings, tox):
        super().__init__(tox)
        self._settings = settings

    def check_permissions(self, command_roles, friend_number):
        friend_roles = self.get_user_roles(friend_number)
        return any(friend_role in command_roles for friend_role in friend_roles)

    def get_user_roles(self, friend_number):
        if not self._tox.friend_exists(friend_number):
            return []
        friend_public_key = self._tox.friend_get_public_key(friend_number)
        friend_name = self._tox.friend_get_name(friend_number)
        banned_nicks = self._settings['ban']['nicks']
        banned_public_keys = self._settings['ban']['public_keys']
        if friend_public_key in banned_public_keys or any([nick in friend_name for nick in banned_nicks]):
            return []
        user_roles = self._settings['users']
        return user_roles[friend_public_key] if friend_public_key in user_roles else PermissionChecker.DEFAULT_ROLES

    def accept_request_from(self, public_key):
        return self._settings['accept_requests'] and public_key not in self._settings['ban']['public_keys']

    def accept_gc_invite_from(self, friend_number):
        return 'admin' in self.get_user_roles(friend_number)


class PermissionsException(Exception):

    def __init__(self, friend_number, command):
        self._friend_number = friend_number
        self._command = command

    def __str__(self):
        return 'Friend number: {}, command: {}'.format(self._friend_number, self._command)


def authorize(method):

    def wrapped(self, roles, friend_number, *args):
        self.check_permissions(method.__name__, roles, friend_number)
        method(self, friend_number, *args)

    return wrapped
