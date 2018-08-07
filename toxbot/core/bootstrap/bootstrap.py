import random
import urllib.request
from core.util import log, get_abs_file_path
import json
import os.path


class Node:

    def __init__(self, node):
        self._ip, self._port, self._tox_key = node['ipv4'], node['port'], node['public_key']
        self._priority = random.randint(1, 1000000) if node['status_tcp'] and node['status_udp'] else 0

    def get_priority(self):
        return self._priority

    priority = property(get_priority)

    def get_data(self):
        return bytes(self._ip, 'utf-8'), self._port, self._tox_key


def generate_nodes():
    with open(get_abs_file_path('nodes.json', __file__), 'rt') as fl:
        json_nodes = json.loads(fl.read())['nodes']
    nodes = map(lambda json_node: Node(json_node), json_nodes)
    sorted_nodes = sorted(nodes, key=lambda x: x.priority)[-4:]
    for node in sorted_nodes:
        yield node.get_data()


def save_nodes(nodes):
    if not nodes:
        return
    print('Saving nodes...')
    with open(get_abs_file_path('nodes.json', __file__), 'wb') as fl:
        fl.write(nodes)


def download_nodes_list():
    try:
        url = 'https://nodes.tox.chat/json'
        req = urllib.request.Request(url)
        req.add_header('Content-Type', 'application/json')
        response = urllib.request.urlopen(req)
        result = response.read()
        save_nodes(result)
    except Exception as ex:
        log('TOX nodes loading error: ' + str(ex))
