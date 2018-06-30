from core.commands.default_commands import *
from core.permissions_checker import *
from core.util import log


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

    def interpret_gc_message(self, message, gc_number, peer_number):
        message = message.strip()
        command = self._get_gc_command(message, gc_number, peer_number)
        self._execute_command(command)

    def interpret_gc_private_message(self, message, gc_number, peer_number):
        message = message.strip()
        command = self._get_gc_private_command(message, gc_number, peer_number)
        self._execute_command(command)

    # -----------------------------------------------------------------------------------------------------------------
    # Commands loading
    # -----------------------------------------------------------------------------------------------------------------

    def _get_command(self, message, friend_number):
        command = self._parse_command(message, friend_number)

        return command or InvalidCommand(self._bot, friend_number)

    def _get_gc_command(self, message, gc_number, peer_number):
        command = self._parse_gc_command(message,gc_number, peer_number)

        return command or InvalidGcCommand(self._bot, gc_number, peer_number)

    def _get_gc_private_command(self, message, gc_number, peer_number):
        command = self._parse_gc_private_command(message, gc_number, peer_number)

        return command or InvalidGcPrivateCommand(self._bot, gc_number, peer_number)

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
                if status < 0 or status > 2:
                    raise ValueError()
                return self._create_command(friend_number, 'status', status)
            except ValueError:
                return
        elif message.startswith('status_message '):
            new_status_message = message[len('status_message '):]
            return self._create_command(friend_number, 'status_message', new_status_message)
        elif message in ('id', 'info'):
            return self._create_command(friend_number, message)

    def _parse_gc_command(self, message, gc_number, peer_number):
        pass

    def _parse_gc_private_command(self, message, gc_number, peer_number):
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
