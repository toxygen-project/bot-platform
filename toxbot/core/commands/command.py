class CommandData:

    def __init__(self, method_name, allowed_roles, description=''):
        self._method_name = method_name
        self._allowed_roles = allowed_roles
        self._description = description

    def get_method_name(self):
        return self._method_name

    method_name = property(get_method_name)

    def get_roles(self):
        return self._allowed_roles

    roles = property(get_roles)

    def get_description(self):
        return self._description

    description = property(get_description)


_commands = {
    'name': CommandData('set_name', ['admin'], 'Sets my name'),
    'status': CommandData('set_status', ['admin'], 'Sets my status'),
    'status_message': CommandData('set_status_message', ['admin'], 'Sets my status message'),
    'id': CommandData('get_id', ['user'], 'Gets my TOX ID'),
    'info': CommandData('get_info', ['user'], 'Print my current status'),
    'help': CommandData('print_help', ['user'], 'Prints commands list'),
}


def get_commands_descriptions():
    s = ''
    for key in _commands:
        s += '{}: {}\n'.format(key, _commands[key].description)
    return s


def extend_command_list(new_commands):
    _commands.update(new_commands)


class Command:

    def __init__(self, bot, friend_number, command, *arguments):
        self._bot = bot
        self._friend_number = friend_number
        self._command = command
        self._arguments = arguments

    def execute(self):
        if self._command in _commands:
            command_data = _commands[self._command]
            method = self._bot[command_data.method_name]
            method(command_data.roles, self._friend_number, *self._arguments)
        else:
            self._bot.invalid_command(self._friend_number)
            print('Unknown command: ' + self._command)
