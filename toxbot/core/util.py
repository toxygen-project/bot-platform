import os.path
import time


def curr_directory():
    return os.path.dirname(os.path.realpath(__file__))


def log(data):
    print(data)
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


def time_from_seconds(seconds):
    return time.strftime('%D days %H hours %M minutes %S seconds', time.gmtime(seconds))


def get_time():
    return int(time.time())
