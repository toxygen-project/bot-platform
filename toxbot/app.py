from core.bootstrap.bootstrap import generate_nodes, download_nodes_list
from middleware.callbacks import init_callbacks
import sys
from time import sleep
from core.bot_data.profile_manager import ProfileManager
from middleware.tox_factory import *
from core.bot_data.settings import Settings
import core.util as util
from app_parameters import *

__version__ = '0.2'
__maintainer__ = 'Ingvar'


class ToxBotApplication:

    def __init__(self, profile_path):
        self._path = profile_path

        self._tox = self._file_transfer_handler = self._bot = self._profile_manager = None
        self._interpreter = self._settings = self._parameters = self._permission_checker = None
        self._stop = False

    def main(self, parameters=None):
        self._parameters = parameters or ToxBotAppParameters()

        util.log('Starting ToxBot v' + __version__)

        self._create_dependencies()

        self._init_callbacks()
        self._bootstrap()

        try:
            while not self._stop:
                self._tox.iterate()
                sleep(self._tox.iteration_interval() / 1000)
        except KeyboardInterrupt:
            print('Closing...')

        self._settings.save()
        self._profile_manager.save_profile()
        del self._tox

    def _stop(self):
        self._stop = True

    def _reconnect(self):
        self._profile_manager.save_profile()
        profile_data = self._profile_manager.load_profile()
        self._tox = tox_factory(profile_data, self._settings)
        
        tox_savers = [self._bot, self._file_transfer_handler, self._profile_manager,
                      self._permission_checker]
        for tox_saver in tox_savers:
            tox_saver.set_tox(self._tox)

        self._init_callbacks()
        self._bootstrap()

    def _create_dependencies(self):
        self._profile_manager = ProfileManager(self._path)
        profile_data = self._profile_manager.load_profile()
        settings_path = self._profile_manager.get_settings_path()
        self._settings = Settings(settings_path)
        self._tox = tox_factory(profile_data, self._settings)
        self._profile_manager.set_tox(self._tox)
        self._permission_checker = PermissionChecker(self._settings, self._tox)

        self._file_transfer_handler = self._parameters.file_transfer_handler_factory(self._tox,
                                                                                     self._permission_checker)
        self._bot = self._parameters.bot_factory(self._tox, self._settings, self._profile_manager,
                                                 self._permission_checker, self._file_transfer_handler,
                                                 self._stop, self._reconnect)
        self._interpreter = self._parameters.interpreter_factory(self._bot)

    def _init_callbacks(self):
        init_callbacks(self._bot, self._tox, self._interpreter, self._file_transfer_handler,
                       self._parameters.should_use_old_gc)
        if self._parameters.callbacks_initializer is not None:
            self._parameters.callbacks_initializer(self._bot, self._tox, self._interpreter,
                                                   self._file_transfer_handler, self._parameters.should_use_old_gc)

    def _bootstrap(self):
        if self._settings['download_nodes']:
            download_nodes_list()
        for data in generate_nodes():
            self._tox.bootstrap(*data)


def run_app(profile_path):
    app = ToxBotApplication(profile_path)
    app.main()


def main():
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = util.get_default_path()

    run_app(path)


if __name__ == '__main__':
    main()
