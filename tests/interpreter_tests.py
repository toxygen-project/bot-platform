from toxbot.wrapper.toxcore_enums_and_consts import TOX_USER_STATUS
from toxbot.core.factories import interpreter_default_factory
from tests.common import FRIEND_NUMBER


class FakeBot:

    def __init__(self):
        self.set_status_called = 0
        self.set_name_called = 0

    def set_status(self, _, friend_number, status):
        assert friend_number == FRIEND_NUMBER
        assert status in TOX_USER_STATUS.values()
        self.set_status_called += 1

    def set_name(self, _, friend_number, name):
        assert friend_number == FRIEND_NUMBER
        assert name
        self.set_name_called += 1


class TestInterpreter:

    def test_commands(self):
        bot = self._create_bot()
        interpreter = interpreter_default_factory(bot)

        for status_command in ('status 123', 'status -1', ' status 2', 'status 0    '):
            interpreter.interpret(status_command, FRIEND_NUMBER)
        assert bot.set_status_called == 2

        for name_command in ('name', 'name 123', ' name '):
            interpreter.interpret(name_command, FRIEND_NUMBER)
        assert bot.set_name_called == 1

    @staticmethod
    def _create_bot():
        return FakeBot()
