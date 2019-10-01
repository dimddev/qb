"""
Auth module
"""
import base64
from typing import Callable


class AuthToken:
    """Auth"""
    def __init__(self, auth_cred: str):
        self.auth_cred = auth_cred
        self.header = {'Authorization': None}

    def get_header(self) -> dict:
        """get_header

        :rtype: dict
        """
        self.header['Authorization'] = 'token {}'.format(self.auth_cred)
        return self.header


class AuthBasic(AuthToken):
    """BasicAuth"""
    def get_header(self) -> dict:
        """get_header

        :rtype: dict
        """
        self.header['Authorization'] = 'Basic {}'.format(
            base64.b64encode(self.auth_cred.encode('utf-8')).decode())

        return self.header


def auth_factory(auth_type: str) -> Callable:
    """auth_factory

    :param auth_type:
    :type auth_type: str
    :rtype: Callable
    """

    auth_factories = {
        'basic': AuthBasic,
        'token': AuthToken
    }

    return auth_factories.get(auth_type.lower())

__ALL__ = [
    'auth_factory'
]
