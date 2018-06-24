from core.factories import *


class ToxBotAppParameters:

    def __init__(self,
                 bot_factory=bot_default_factory,
                 interpreter_factory=interpreter_default_factory,
                 file_transfer_handler_factory=file_transfer_handler_default_factory,
                 should_use_old_gc=True,
                 callbacks_initializer=None):
        self._bot_factory = bot_factory
        self._interpreter_factory = interpreter_factory
        self._file_transfer_handler_factory = file_transfer_handler_factory
        self._should_use_old_gc = should_use_old_gc
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

    def get_should_use_old_gc(self):
        return self._should_use_old_gc

    should_use_old_gc = property(get_should_use_old_gc)

    def get_callbacks_initializer(self):
        return self._callbacks_initializer

    callbacks_initializer = property(get_callbacks_initializer)
