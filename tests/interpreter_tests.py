from toxbot.wrapper.toxcore_enums_and_consts import TOX_USER_STATUS
from toxbot.core.factories import interpreter_default_factory
from toxbot.core.commands.command import CommandsList
from tests.common import FRIEND_NUMBER


# TODO: test all commands

class FakeBot:

    def __init__(self):
        self.set_status_called = 0
        self.set_name_called = 0
        self.get_id_called = 0

    def set_status(self, _, friend_number, status):
        assert friend_number == FRIEND_NUMBER
        assert status in TOX_USER_STATUS.values()
        self.set_status_called += 1

    def set_name(self, _, friend_number, name):
        assert friend_number == FRIEND_NUMBER
        assert name
        self.set_name_called += 1

    def get_id(self, _, friend_number):
        assert friend_number == FRIEND_NUMBER
        self.get_id_called += 1


class TestInterpreter:

    def test_commands(self):
        bot = self._create_bot()
        commands_list = CommandsList()
        interpreter = interpreter_default_factory(bot, commands_list)

        for status_command in ('status 123', 'status -1', ' status 2', 'status 0    '):
            interpreter.interpret(status_command, FRIEND_NUMBER)
        assert bot.set_status_called == 2

        for name_command in ('name', 'name 123', ' name '):
            interpreter.interpret(name_command, FRIEND_NUMBER)
        assert bot.set_name_called == 1

        for id_command in ('id', 'id,', '  id', '\tid'):
            interpreter.interpret(id_command, FRIEND_NUMBER)
        assert bot.get_id_called == 3

    @staticmethod
    def _create_bot():
        return FakeBot()
