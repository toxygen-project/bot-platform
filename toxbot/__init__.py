import os
import sys


# TODO: recursive add all
path = os.path.dirname(os.path.realpath(__file__))  # curr dir

sys.path.insert(0, os.path.join(path, 'wrapper'))
sys.path.insert(0, os.path.join(path, 'core'))
sys.path.insert(0, path)
