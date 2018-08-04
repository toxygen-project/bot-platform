from wrapper.toxcore_enums_and_consts import *
from wrapper.tox import bin_to_string

from core.file_transfers.file_transfer_thread import execute

# -----------------------------------------------------------------------------------------------------------------
# Callbacks - current user
# -----------------------------------------------------------------------------------------------------------------


def self_connection_status(bot):
    """
    Current user changed connection status (offline, UDP, TCP)
    """
    def wrapped(tox, connection_status, user_data):
        print('Connection status: ', str(connection_status))
        bot.update_connection_status(connection_status)

    return wrapped


# -----------------------------------------------------------------------------------------------------------------
# Callbacks - friends
# -----------------------------------------------------------------------------------------------------------------


def friend_status(file_transfer_handler):
    def wrapped(tox, friend_number, new_status, user_data):
        file_transfer_handler.send_avatar(friend_number)

    return wrapped


def friend_message(interpreter):
    """
    New message from friend
    """
    def wrapped(tox, friend_number, message_type, message, size, user_data):
        message = str(message, 'utf-8')
        interpreter.interpret(message, friend_number)

    return wrapped


def friend_request(bot):
    def wrapped(tox, public_key, message, message_size, user_data):
        """
        Called when user get new friend request
        """
        key = ''.join(chr(x) for x in public_key[:TOX_PUBLIC_KEY_SIZE])
        tox_pk = bin_to_string(key, TOX_PUBLIC_KEY_SIZE)
        message = str(message[:message_size], 'utf-8')
        print('Friend request', tox_pk)
        bot.process_friend_request(tox_pk, message)

    return wrapped

# -----------------------------------------------------------------------------------------------------------------
# Callbacks - file transfers
# -----------------------------------------------------------------------------------------------------------------


def tox_file_recv(file_transfer_handler):
    """
    New incoming file
    """
    def wrapped(tox, friend_number, file_number, file_type, file_size, file_name, file_name_size, user_data):
        if file_type == TOX_FILE_KIND['DATA']:
            print('File')
            try:
                file_name = str(file_name[:file_name_size], 'utf-8')
            except:
                file_name = 'tox_file'
            file_transfer_handler.process_incoming_transfer(friend_number, file_number, file_name, file_size)
        else:  # AVATAR
            print('Incoming avatar')
            file_transfer_handler.cancel_transfer(friend_number, file_number)

    return wrapped


def file_recv_chunk(file_transfer_handler):
    """
    Incoming chunk
    """
    def wrapped(tox, friend_number, file_number, position, chunk, length, user_data):
        execute(file_transfer_handler.incoming_chunk, friend_number, file_number, position,
                chunk[:length] if length else None)

    return wrapped


def file_chunk_request(file_transfer_handler):
    """
    Outgoing chunk
    """
    def wrapped(tox, friend_number, file_number, position, size, user_data):
        execute(file_transfer_handler.outgoing_chunk, friend_number, file_number, position, size)

    return wrapped


def file_recv_control(file_transfer_handler):
    """
    Friend cancelled, paused or resumed file transfer
    """
    def wrapped(tox, friend_number, file_number, file_control, user_data):
        if file_control == TOX_FILE_CONTROL['CANCEL']:
            file_transfer_handler.transfer_cancelled(friend_number, file_number)
        elif file_control == TOX_FILE_CONTROL['PAUSE']:
            file_transfer_handler.pause_transfer(friend_number, file_number, True)
        elif file_control == TOX_FILE_CONTROL['RESUME']:
            file_transfer_handler.resume_transfer(friend_number, file_number, True)

    return wrapped

# -----------------------------------------------------------------------------------------------------------------
# Callbacks - new group chats
# -----------------------------------------------------------------------------------------------------------------


def group_invite(bot):
    def wrapped(tox, friend_number, invite_data, length, user_data):
        bot.process_gc_invite_request(friend_number, bytes(invite_data[:length]))

    return wrapped


def group_message(interpreter):
    """
    New message in group chat
    """
    def wrapped(tox_link, group_number, peer_id, message_type, message, length, user_data):
        interpreter.interpret_gc_message(message[:length], group_number, peer_id)

    return wrapped


def group_private_message(interpreter):
    """
    New message in group chat
    """

    def wrapped(tox_link, group_number, peer_id, message_type, message, length, user_data):
        interpreter.interpret_gc_private_message(message[:length], group_number, peer_id)

    return wrapped


# -----------------------------------------------------------------------------------------------------------------
# Callbacks - old group chats
# -----------------------------------------------------------------------------------------------------------------

def conference_invite(bot):
    def wrapped(tox, friend_number, invite_data, length, user_data):
        bot.process_conference_invite_request(friend_number, bytes(invite_data[:length]))

    return wrapped


def conference_message(interpreter):
    def wrapped(tox, group_number, peer_number, message, length, user_data):
        interpreter.interpret_gc_message(message[:length], group_number, peer_number)

    return wrapped


# -----------------------------------------------------------------------------------------------------------------
# Callbacks - initialization
# -----------------------------------------------------------------------------------------------------------------


def init_callbacks(bot, tox, interpreter, file_transfer_handler, should_use_old_gc):
    """
    Initialization of all callbacks.
    :param bot: Bot instance
    :param tox: Tox instance
    :param interpreter: Interpreter instance
    :param file_transfer_handler: FileTransfersHandler instance
    :param should_use_old_gc: bool value. True if we should run app with old gc support
    """
    tox.callback_self_connection_status(self_connection_status(bot))

    tox.callback_friend_status(friend_status(file_transfer_handler))
    tox.callback_friend_message(friend_message(interpreter))
    tox.callback_friend_request(friend_request(bot))

    tox.callback_file_recv(tox_file_recv(file_transfer_handler))
    tox.callback_file_recv_chunk(file_recv_chunk(file_transfer_handler))
    tox.callback_file_chunk_request(file_chunk_request(file_transfer_handler))
    tox.callback_file_recv_control(file_recv_control(file_transfer_handler))

    if should_use_old_gc:
        tox.callback_conference_invite(conference_invite(bot))
        tox.callback_conference_message(conference_message(interpreter))
    else:
        tox.callback_group_invite(group_invite(bot), 0)
        tox.callback_group_message(group_message(interpreter), 0)
        tox.callback_group_private_message(group_private_message(interpreter), 0)
