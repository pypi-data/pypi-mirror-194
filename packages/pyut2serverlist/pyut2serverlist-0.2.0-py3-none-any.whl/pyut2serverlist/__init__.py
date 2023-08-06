from .connection import Connection
from .exceptions import Error, ConnectionError, TimeoutError, AuthError
from .filter import Filter, Comparator
from .principalserver import PrincipalServer, Game
from .server import Server

"""
pyut2serverlist.

Simple Python library for querying Unreal Engine 2 based principal servers and their game servers.
"""

__version__ = '0.2.0'
__author__ = 'cetteup'
__credits__ = [
    'https://github.com/CVSoft/MSQuery',
    'https://github.com/Austinb/GameQ',
    'https://github.com/gamedig/node-gamedig'
]
__all__ = [
    'Connection', 'PrincipalServer', 'Server', 'Game', 'Filter', 'Comparator',
    'Error', 'ConnectionError', 'TimeoutError', 'AuthError'
]
