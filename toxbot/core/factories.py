from core.interpreter import *
from core.bot import *
from core.file_transfers.file_transfers_handler import *
from core.groups.new_group_service import NewGroupService
from core.groups.old_group_service import OldGroupService


def interpreter_default_factory(bot, commands_list):
    return Interpreter(bot, commands_list)


def bot_default_factory(tox, settings, profile_manager, permission_checker, file_transfer_handler,
                        group_service, stop_action, reconnect_action):
    return Bot(tox, settings, profile_manager, permission_checker, file_transfer_handler,
               group_service, stop_action, reconnect_action)


def file_transfer_handler_default_factory(tox, permission_checker):
    return FileTransfersHandler(tox, permission_checker)


def group_service_default_factory(tox, should_use_old_gc):
    return OldGroupService(tox) if should_use_old_gc else NewGroupService(tox)
