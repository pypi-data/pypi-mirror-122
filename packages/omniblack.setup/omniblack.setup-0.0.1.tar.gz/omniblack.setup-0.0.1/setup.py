from os.path import dirname, realpath
from sys import path

dir = dirname(realpath(__file__))

try:
    path.append(dir)
    from omniblack.setup import setup
    setup()
finally:
    path.remove(dir)

