from core.permissions_checker import *
from wrapper.toxcore_enums_and_consts import *
import time


class Bot:

    def __init__(self, tox, settings, profile_manager, permission_cheker):
        self._tox = tox
        self._settings = settings
        self._profile_manager = profile_manager
        self._permission_checker = permission_cheker
        self._start_time = int(time.time())

    def check_permissions(self, command, roles, friend_number):
        if not self._permission_checker.check_permissions(roles, friend_number):
            raise PermissionsException(friend_number, command)

    def process_friend_request(self, public_key):
        if self._permission_checker.accept_request_from(public_key):
            self._tox.friend_add_norequest(public_key)
            self._profile_manager.save_profile()

    def update_connection_status(self, connection_status):
        pass

    def send_message_to_friend(self, friend_number, message_type, message):
        """
        :param friend_number: friend number
        :param message_type: type of message
        :param message: message text
        """
        messages = self.split_message(message)
        for tox_message in messages:
            self._tox.friend_send_message(friend_number, message_type, tox_message)

    def send_message_to_group(self, group_number, message_type, message):
        """
        :param group_number: group number
        :param message_type: type of message
        :param message: message text
        """
        messages = self.split_message(message)
        for tox_message in messages:
            self._tox.group_send_message(group_number, message_type, tox_message)

    def split_message(self, message):
        messages = []
        while len(message) > TOX_MAX_MESSAGE_LENGTH:
            size = TOX_MAX_MESSAGE_LENGTH * 4 / 5
            last_part = message[size:TOX_MAX_MESSAGE_LENGTH]
            if ' ' in last_part:
                index = last_part.index(' ')
            elif ',' in last_part:
                index = last_part.index(',')
            elif '.' in last_part:
                index = last_part.index('.')
            else:
                index = TOX_MAX_MESSAGE_LENGTH - size - 1
            index += size + 1
            messages.append(message[:index])
            message = message[index:]

        return messages

    # -----------------------------------------------------------------------------------------------------------------
    # Bot methods
    # -----------------------------------------------------------------------------------------------------------------

    def invalid_command(self, friend_number):
        self.send_message_to_friend(friend_number, TOX_MESSAGE_TYPE['NORMAL'], 'Invalid command.')

    @authorize
    def set_name(self, friend_number, name):
        self._tox.self_set_name(name)

    @authorize
    def set_status(self, friend_number, status):
        self._tox.self_set_status(status)

    @authorize
    def set_status_message(self, friend_number, status_message):
        self._tox.self_set_status_message(status_message)

    @authorize
    def get_id(self, friend_number):
        tox_id = self._tox.self_get_address()
        self.send_message_to_friend(friend_number, TOX_MESSAGE_TYPE['NORMAL'], tox_id)

    @authorize
    def get_info(self, friend_number):
        pass

    @authorize
    def remove_friend_by_public_key(self, friend_number, public_key):
        pass

    @authorize
    def send_message(self, friend_number, message, destination_friend=None):
        pass

    @authorize
    def send_group_message(self, friend_number, message, destination_group=None):
        pass

    @authorize
    def stop(self, friend_number):
        pass

    @authorize
    def set_roles_of_friend_by_public_key(self, friend_number, public_key, roles):
        pass

    def get_friend_roles(self, friend_number):
        pass

    @authorize
    def ban_nick(self, friend_number, nick):
        pass

    @authorize
    def ban_public_key(self, friend_number, public_key):
        pass

    def print_help(self, friend_number, help):
        self.send_message_to_friend(friend_number, TOX_MESSAGE_TYPE['NORMAL'], help)
