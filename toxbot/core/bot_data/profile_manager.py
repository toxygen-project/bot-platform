import os.path
import core.util as util


class ProfileManager(util.ToxSave):

    def __init__(self, profile_path):
        super().__init__(None)
        self._path = profile_path

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
        print('Profile was saved successfully')

    def get_settings_path(self):
        return self._path.replace('.tox', '.json')
