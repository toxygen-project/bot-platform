from toxbot.app_parameters import ToxBotAppParameters
from toxbot.app import ToxBotApplication
from toxbot.core.bot import Bot
from toxbot.core.interpreter import Interpreter
from toxbot.core.commands.command import extend_command_list, CommandData, Command
from toxbot.core.permissions_checker import authorize


class Echobot(Bot):

    @authorize
    def echo(self, friend_number, message):
        super().send_message_to_friend(friend_number, message)


def bot_factory(tox, settings, profile_manager, permission_checker, stop_action, reconnect_action):
    return Echobot(tox, settings, profile_manager, permission_checker, stop_action, reconnect_action)


class EchobotInterpreter(Interpreter):

    def _parse_command(self, message, friend_number):
        command = super()._parse_command(message, friend_number)
        if not command.is_valid:
            command = Command(self._bot, friend_number, 'echo', message)

        return command


def main():
    extend_command_list({
        'echo': CommandData('echo', ['user', 'admin'])
    })
    app = ToxBotApplication('echobot.tox')
    params = ToxBotAppParameters(interpreter_factory=lambda bot: EchobotInterpreter(bot),
                                 bot_factory=bot_factory)
    app.main(params)


if __name__ == '__main__':
    main()
