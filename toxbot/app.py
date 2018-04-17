from core.bootstrap.bootstrap import generate_nodes, download_nodes_list
from middleware.callbacks import init_callbacks
import sys
from core.bot_data.profile_manager import ProfileManager
from middleware.tox_factory import *
from core.bot_data.settings import Settings
from core.factories import *
import core.util as util
import time

__version__ = '0.2'
__maintainer__ = 'Ingvar'


class ToxBotAppParameters:

    def __init__(self,
                 bot_factory=bot_default_factory,
                 interpreter_factory=interpreter_default_factory,
                 file_transfer_handler_factory=file_transfer_handler_default_factory,
                 callbacks_initializer=None):
        self._bot_factory = bot_factory
        self._interpreter_factory = interpreter_factory
        self._file_transfer_handler_factory = file_transfer_handler_factory
        self._callbacks_initializer = callbacks_initializer

    def get_bot_factory(self):
        return self._bot_factory

    bot_factory = property(get_bot_factory)

    def get_interpreter_factory(self):
        return self._interpreter_factory

    interpreter_factory = property(get_interpreter_factory)

    def get_file_transfer_handler_factory(self):
        return self._file_transfer_handler_factory

    file_transfer_handler_factory = property(get_file_transfer_handler_factory)

    def get_callbacks_initializer(self):
        return self._callbacks_initializer

    callbacks_initializer = property(get_callbacks_initializer)


class ToxBotApplication:

    def __init__(self, profile_path):
        self._tox = None
        self._stop = False
        self._bot = None
        self._path = profile_path

    def main(self, parameters=None):
        if parameters is None:
            parameters = ToxBotAppParameters()

        print('Starting ToxBot v' + __version__)
        profile_manager = ProfileManager(self._path)
        profile_data = profile_manager.load_profile()
        settings_path = profile_manager.get_settings_path()
        settings = Settings(settings_path)
        self._tox = tox_factory(profile_data, settings)
        profile_manager.set_tox(self._tox)
        permission_checker = PermissionChecker(settings, self._tox)

        file_transfer_handler = parameters.file_transfer_handler_factory(self._tox, permission_checker)
        self._bot = parameters.bot_factory(self._tox, settings, profile_manager, permission_checker, self.stop)
        interpreter = parameters.interpreter_factory(self._bot)

        init_callbacks(self._bot, self._tox, interpreter, file_transfer_handler)
        if parameters.callbacks_initializer is not None:
            parameters.callbacks_initializer(self._bot, self._tox, interpreter, file_transfer_handler)

        # bootstrap
        if settings['download_nodes']:
            download_nodes_list()
        for data in generate_nodes():
            self._tox.bootstrap(*data)

        try:
            while not self._stop:
                self._tox.iterate()
                time.sleep(self._tox.iteration_interval() / 1000)
        except KeyboardInterrupt:
            print('Closing...')

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
