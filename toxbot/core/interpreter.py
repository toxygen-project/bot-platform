from core.commands.default_commands import *
from core.permissions_checker import *
from core.util import log
from wrapper.toxcore_enums_and_consts import *


class Interpreter:

    def __init__(self, bot):
        self._bot = bot

    # -----------------------------------------------------------------------------------------------------------------
    # Interpretation
    # -----------------------------------------------------------------------------------------------------------------

    def interpret(self, message, friend_number):
        message = message.strip()
        command = self._get_command(message, friend_number)
        self._execute_command(command)

    def interpret_gc_message(self, message, gc_number, peer_id):
        message = message.strip()
        command = self._get_gc_command(message, gc_number, peer_id)
        self._execute_command(command)

    def interpret_gc_private_message(self, message, gc_number, peer_id):
        message = message.strip()
        command = self._get_gc_private_command(message, gc_number, peer_id)
        self._execute_command(command)

    # -----------------------------------------------------------------------------------------------------------------
    # Commands loading
    # -----------------------------------------------------------------------------------------------------------------

    def _get_command(self, message, friend_number):
        command = self._parse_command(message, friend_number)

        return command or InvalidCommand(self._bot, friend_number)

    def _get_gc_command(self, message, gc_number, peer_id):
        command = self._parse_gc_command(message,gc_number, peer_id)

        return command or InvalidGcCommand(self._bot, gc_number, peer_id)

    def _get_gc_private_command(self, message, gc_number, peer_id):
        command = self._parse_gc_private_command(message, gc_number, peer_id)

        return command or InvalidGcPrivateCommand(self._bot, gc_number, peer_id)

    # -----------------------------------------------------------------------------------------------------------------
    # Parsing
    # -----------------------------------------------------------------------------------------------------------------

    def _parse_command(self, message, friend_number):
        if message == 'help':
            return HelpCommand(self._bot, friend_number)
        elif message.startswith('name '):
            new_name = message[len('name '):]
            return self._create_command(friend_number, 'name', new_name)
        elif message.startswith('status '):
            new_status = message[len('status '):]
            try:
                status = int(new_status)
                if status < TOX_USER_STATUS['NONE'] or status > TOX_USER_STATUS['BUSY']:
                    raise ValueError()
                return self._create_command(friend_number, 'status', status)
            except ValueError:
                return
        elif message.startswith('status_message '):
            new_status_message = message[len('status_message '):]
            return self._create_command(friend_number, 'status_message', new_status_message)
        elif message in ('id', 'info', 'reconnect', 'roles', 'stop', 'groups'):
            return self._create_command(friend_number, message)
        elif message.startswith('auto_reconnection '):
            reconnection_interval = message[len('auto_reconnection '):]
            try:
                reconnection_interval = int(reconnection_interval)
                if reconnection_interval < 0:
                    raise ValueError()
                return self._create_command(friend_number, 'auto_reconnection', reconnection_interval)
            except ValueError:
                return
        elif message.startswith('ban pk '):
            public_key = message[len('ban pk '):]
            if len(public_key) == TOX_PUBLIC_KEY_SIZE * 2:
                return self._create_command(friend_number, 'ban pk', public_key)
        elif message.startswith('ban nick '):
            nick = message[len('ban pk '):]
            return self._create_command(friend_number, 'ban nick', nick)
        elif message.startswith('leave ') or message.startswith('invite '):
            try:
                command, group_number_str = message.split()
                group_number = int(group_number_str)
                if group_number < 0:
                    raise ValueError
                return self._create_command(friend_number, command, group_number)
            except ValueError:
                return

        return None  # command was not found

    def _parse_gc_command(self, message, gc_number, peer_id):
        pass

    def _parse_gc_private_command(self, message, gc_number, peer_id):
        pass

    # -----------------------------------------------------------------------------------------------------------------
    # Other private methods
    # -----------------------------------------------------------------------------------------------------------------

    def _create_command(self, friend_number, name, *arguments):
        return Command(self._bot, friend_number, name, *arguments)

    @staticmethod
    def _execute_command(command):
        try:
            command.execute()
        except PermissionsException as ex:
            log('Permissions error: ' + str(ex))
        except Exception as ex:
            log('Exception: ' + str(ex))
