from wrapper.toxcore_enums_and_consts import TOX_FILE_KIND, TOX_FILE_CONTROL
from os.path import basename, getsize
from os import remove, rename
from time import time
from wrapper.tox import Tox


FILE_TRANSFER_STATE = {
    'RUNNING': 0,
    'PAUSED_BY_USER': 1,
    'CANCELLED': 2,
    'FINISHED': 3,
    'PAUSED_BY_FRIEND': 4,
    'INCOMING_NOT_STARTED': 5,
    'OUTGOING_NOT_STARTED': 6,
    'UNSENT': 7
}


class FileTransfer:
    """
    Superclass for file transfers
    """

    def __init__(self, path, tox, friend_number, size, file_number=None):
        self._path = path
        self._tox = tox
        self._friend_number = friend_number
        self._state = FILE_TRANSFER_STATE['RUNNING']
        self._file_number = file_number
        self._creation_time = None
        self._size = float(size)
        self._done = 0
        self._file_id = self._file = None

    def get_file_number(self):
        return self._file_number

    file_number = property(get_file_number)

    def get_state(self):
        return self._state

    def set_state(self, value):
        self._state = value

    state = property(get_state, set_state)

    def get_friend_number(self):
        return self._friend_number

    friend_number = property(get_friend_number)

    def get_file_id(self):
        return self._file_id

    file_id = property(get_file_id)

    def get_path(self):
        return self._path

    path = property(get_path)

    def get_size(self):
        return self._size

    size = property(get_size)

    def cancel(self):
        self.send_control(TOX_FILE_CONTROL['CANCEL'])
        if self._file is not None:
            self._file.close()

    def cancelled(self):
        if self._file is not None:
            self._file.close()
        self.state = FILE_TRANSFER_STATE['CANCELLED']

    def pause(self, by_friend):
        if not by_friend:
            self.send_control(TOX_FILE_CONTROL['PAUSE'])
        else:
            self.state = FILE_TRANSFER_STATE['PAUSED_BY_FRIEND']

    def send_control(self, control):
        if self._tox.file_control(self._friend_number, self._file_number, control):
            self.state = control

    def get_file_id(self):
        return self._tox.file_get_file_id(self._friend_number, self._file_number)

# -----------------------------------------------------------------------------------------------------------------
# Send file
# -----------------------------------------------------------------------------------------------------------------


class SendTransfer(FileTransfer):

    def __init__(self, path, tox, friend_number, kind=TOX_FILE_KIND['DATA'], file_id=None):
        if path is not None:
            fl = open(path, 'rb')
            size = getsize(path)
        else:
            fl = None
            size = 0
        super().__init__(path, tox, friend_number, size)
        self._file = fl
        self.state = FILE_TRANSFER_STATE['OUTGOING_NOT_STARTED']
        self._file_number = tox.file_send(friend_number, kind, size, file_id,
                                          bytes(basename(path), 'utf-8') if path else b'')
        self._file_id = self.get_file_id()

    def send_chunk(self, position, size):
        """
        Send chunk
        :param position: start position in file
        :param size: chunk max size
        """
        if self._creation_time is None:
            self._creation_time = time()
        if size:
            self._file.seek(position)
            data = self._file.read(size)
            self._tox.file_send_chunk(self._friend_number, self._file_number, position, data)
            self._done += size
        else:
            if self._file is not None:
                self._file.close()
            self.state = FILE_TRANSFER_STATE['FINISHED']


class SendAvatar(SendTransfer):
    """
    Send avatar to friend. Doesn't need file transfer item
    """

    def __init__(self, path, tox, friend_number):
        if path is None:
            avatar_hash = None
        else:
            with open(path, 'rb') as fl:
                avatar_hash = Tox.hash(fl.read())
        super().__init__(path, tox, friend_number, TOX_FILE_KIND['AVATAR'], avatar_hash)


# -----------------------------------------------------------------------------------------------------------------
# Receive file
# -----------------------------------------------------------------------------------------------------------------


class ReceiveTransfer(FileTransfer):

    def __init__(self, path, tox, friend_number, size, file_number, position=0):
        super().__init__(path + '.tmp', tox, friend_number, size, file_number)
        self._file = open(self._path, 'wb')
        self._file_size = position
        self._file.truncate(position)
        self._missed = set()
        self._file_id = self.get_file_id()
        self._done = position

    def cancel(self):
        super().cancel()
        remove(self._path)

    def total_size(self):
        self._missed.add(self._file_size)

        return min(self._missed)

    def write_chunk(self, position, data):
        """
        Incoming chunk
        :param position: position in file to save data
        :param data: raw data (string)
        """
        if self._creation_time is None:
            self._creation_time = time()
        if data is None:
            self._file.close()
            rename(self._path, self._path[:-4])
            self.state = FILE_TRANSFER_STATE['FINISHED']
        else:
            data = bytearray(data)
            if self._file_size < position:
                self._file.seek(0, 2)
                self._file.write(b'\0' * (position - self._file_size))
                self._missed.add(self._file_size)
            else:
                self._missed.discard(position)
            self._file.seek(position)
            self._file.write(data)
            l = len(data)
            if position + l > self._file_size:
                self._file_size = position + l
            self._done += l
