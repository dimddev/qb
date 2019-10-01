"""
A Request module
"""

from dataclasses import dataclass
from typing import Callable

from qbapi.auth import auth_factory


@dataclass
class CreateRequest:
    """RequestData"""
    __data: dict

    def __init__(self, url, auth_cred: str, method: Callable):
        """__init__

        :param auth_cred:
        :type auth_cred: str
        :param method:
        :type method: Callable
        """

        self.__data = {
            'headers': method(auth_cred).get_header(),
            'url': url
        }

    def get(self) -> tuple:
        """get
        :rtype: tuple
        """
        return self.__data['url'], self.__data['headers']


async def create_request(data: tuple) -> tuple:
    """create_request

    :param data:
    :type data: tuple
    :rtype: tuple
    """

    from_api, to_api = data

    from_keys = from_api.pop()
    to_keys = to_api.pop()

    keys_map = {x[0]: x[1] for x in zip(from_keys, to_keys)}

    from_api_auth = from_api.pop()
    to_api_auth = to_api.pop()

    producer_request = CreateRequest(
        *from_api,
        auth_factory(from_api_auth)
    )

    consumer_request = CreateRequest(
        *to_api,
        auth_factory(to_api_auth)
    )

    return (producer_request, consumer_request, keys_map, )
