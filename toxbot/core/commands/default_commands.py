from core.commands.command import *


class InvalidCommand(Command):

    def __init__(self, bot, friend_number):
        super().__init__(bot, friend_number, 'invalid', 'Invalid command.')


class HelpCommand(Command):

    def __init__(self, bot, friend_number):
        help_text = get_commands_descriptions()
        super().__init__(bot, friend_number, 'help', help_text)
