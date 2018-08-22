import os.path
import time
import platform


def curr_directory(current_file=None):
    return os.path.dirname(os.path.realpath(current_file or __file__))


def log(data):
    print(data)
    logs_file = os.path.join(curr_directory(), 'logs.txt')
    with open(logs_file, 'a') as fl:
        fl.write(str(data) + '\n')


def get_abs_file_path(file_path, file=None):
    return os.path.join(curr_directory(file or __file__), file_path)


def get_base_directory(current_file=None):
    return os.path.dirname(curr_directory(current_file or __file__))


def get_libs_directory():
    return get_app_directory('libs')


def get_app_directory(directory_name):
    return join_path(get_base_directory(), directory_name)


def get_avatar_path():
    return get_abs_file_path('bot_data/avatar.png')


def get_settings_path():
    return get_abs_file_path('bot_data/settings.json')


def get_default_path():
    return get_abs_file_path('bot_data/bot.tox')


def join_path(a, b):
    return os.path.join(a, b)


def time_from_seconds(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)

    return '{} days {} hours {} minutes {} seconds'.format(days, hours, minutes, seconds)


def get_time():
    return int(time.time())


def get_platform():
    return platform.system()
