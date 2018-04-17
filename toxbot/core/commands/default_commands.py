from core.commands.command import *


class InvalidCommand(Command):

    def __init__(self, bot, friend_number):
        super().__init__(bot, friend_number, 'invalid', 'Invalid command.')


class InvalidGcCommand(GcCommand):

    def __init__(self, bot, gc_number, peer_number):
        super().__init__(bot, gc_number, peer_number, 'invalid', 'Invalid gc command.')


class InvalidGcPrivateCommand(GcCommand):

    def __init__(self, bot, gc_number, peer_number):
        super().__init__(bot, gc_number, peer_number, 'invalid', 'Invalid gc private command.')


class HelpCommand(Command):

    def __init__(self, bot, friend_number):
        help_text = get_commands_descriptions()
        super().__init__(bot, friend_number, 'help', help_text)
