import os.path


class ProfileManager():

    def __init__(self, profile_path):
        self._path = profile_path
        self._tox = None

    def load_profile(self):
        if not os.path.exists(self._path):
            return None

        with open(self._path, 'rb') as fl:
            data = fl.read()
        return data

    def save_profile(self):
        data = self._tox.get_savedata()
        with open(self._path, 'wb') as dest:
            dest.write(data)
        print('Profile saved successfully')

    def get_settings_path(self):
        return self._path.replace('.tox', '.json')

    def set_tox(self, tox):
        self._tox = tox
