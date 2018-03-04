import os.path


def curr_directory():
    return os.path.dirname(os.path.realpath(__file__))


def log(data):
    logs_file = os.path.join(curr_directory(), 'logs.txt')
    with open(logs_file, 'a') as fl:
        fl.write(str(data) + '\n')


def get_abs_file_path(file_path):
    return os.path.join(curr_directory(), file_path)


def get_avatar_path():
    return get_abs_file_path('bot_data/avatar.png')


def get_settings_path():
    return get_abs_file_path('bot_data/settings.json')


def get_default_path():
    return get_abs_file_path('bot_data/bot.tox')
