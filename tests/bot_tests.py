from toxbot.core.factories import bot_default_factory
from tests.common import FRIEND_NUMBER


BOT_NAME = 'Bot'
ROLES = []


class FakeTox:

    @staticmethod
    def self_set_name(name):
        assert name == BOT_NAME

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

        return bot_default_factory(tox, None, None, permission_checker, None, None, None, None)
