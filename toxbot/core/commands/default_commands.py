from core.commands.command import *


class InvalidCommand(Command):

    def __init__(self, bot, commands_list, friend_number):
        super().__init__(bot, commands_list,friend_number, 'invalid', 'Invalid command.')


class InvalidGcCommand(GcCommand):

    def __init__(self, bot, commands_list, gc_number, peer_number):
        super().__init__(bot, commands_list, gc_number, peer_number, 'invalid', 'Invalid gc command.')


class InvalidGcPrivateCommand(GcCommand):

    def __init__(self, bot, commands_list, gc_number, peer_number):
        super().__init__(bot, commands_list, gc_number, peer_number, 'invalid', 'Invalid gc private command.')


class HelpCommand(ExecutableCommand):

    def __init__(self, bot, commands_list, friend_number):
        super().__init__(lambda: bot.print_help(friend_number, commands_list))
