from core.bootstrap.bootstrap import generate_nodes, download_nodes_list
from communication.callbacks import init_callbacks
import sys
from core.bot_data.profile_manager import ProfileManager
from communication.tox_factory import *
from core.bot_data.settings import Settings
from core.factories import *
import core.util as util

__version__ = '0.1'
__maintainer__ = 'Ingvar'


class ToxBotApplication:

    def __init__(self, profile_path):
        self._tox = None
        self._stop = False
        self._bot = None
        self._path = profile_path

    def main(self,
             bot_factory=bot_default_factory,
             interpreter_factory=interpreter_default_factory,
             file_transfer_handler_factory=file_transfer_handler_default_factory):
        profile_manager = ProfileManager(self._path)
        profile_data = profile_manager.load_profile()
        settings_path = profile_manager.get_settings_path()
        settings = Settings(settings_path)
        self._tox = tox_factory(profile_data, settings)
        permission_checker = PermissionChecker(settings, self._tox)
        file_transfer_handler = file_transfer_handler_factory(self._tox, permission_checker)
        self._bot = bot_factory(self._tox, settings, profile_manager, permission_checker)
        interpreter = interpreter_factory(self._bot)
        init_callbacks(self._bot, self._tox, interpreter, file_transfer_handler)
        if settings['download_nodes']:
            download_nodes_list()
        # bootstrap
        for data in generate_nodes():
            self._tox.bootstrap(*data)
        try:
            while not self._stop:
                self._tox.iterate()
                time.sleep(self._tox.iteration_interval() / 1000.0)
        except KeyboardInterrupt:
            pass
        settings.save()
        profile_manager.save_profile()
        del self._tox

    def stop(self):
        self._stop = True


def main(profile_path):
    app = ToxBotApplication(profile_path)
    app.main()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = util.get_default_path()
    main(path)
