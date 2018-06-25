from toxbot.app_parameters import ToxBotAppParameters
from toxbot.app import ToxBotApplication
from toxbot.core.interpreter import Interpreter
from toxbot.core.commands.command import ExecutableCommand


class EchobotInterpreter(Interpreter):
    """
    Interpreter of user commands.
    """

    def _parse_command(self, message, friend_number):
        # Remove this section if you don't need basic commands support
        ##############################################################
        command = super()._parse_command(message, friend_number)
        if command.is_valid:
            return command
        ##############################################################

        return ExecutableCommand(lambda: self._bot.send_message_to_friend(friend_number, message))


def main():
    # creates app instance
    app = ToxBotApplication('echobot.tox')
    # overrides default app parameters
    params = ToxBotAppParameters(interpreter_factory=lambda bot: EchobotInterpreter(bot))
    # starts app
    app.main(params)


if __name__ == '__main__':
    main()
