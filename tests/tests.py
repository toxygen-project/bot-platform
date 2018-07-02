from toxbot.core.factories import interpreter_default_factory, bot_default_factory
from wrapper.toxcore_enums_and_consts import TOX_USER_STATUS

# TODO: add more tests

# -----------------------------------------------------------------------------------------------------------------
# Common constants
# -----------------------------------------------------------------------------------------------------------------

FRIEND_NUMBER = 42


# -----------------------------------------------------------------------------------------------------------------
# Test interpreter
# -----------------------------------------------------------------------------------------------------------------

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


# -----------------------------------------------------------------------------------------------------------------
# Test bot
# -----------------------------------------------------------------------------------------------------------------

BOT_NAME = 'Bot'
ROLES = []


class FakeTox:

    @staticmethod
    def self_set_name(name):
        assert str(name, 'utf-8') == BOT_NAME

    @staticmethod
    def self_get_address():
        return str()


class FakePermissionChecker:

    @staticmethod
    def check_permissions(_, friend_number):
        return friend_number == FRIEND_NUMBER


class TestBot:

    def test_set_name(self):
        bot = self._create_bot()
        bot.set_name(ROLES, FRIEND_NUMBER, BOT_NAME)

    @staticmethod
    def _create_bot():
        tox = FakeTox()
        permission_checker = FakePermissionChecker()

        return bot_default_factory(tox, None, None, permission_checker, None, None, None)
