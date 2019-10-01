"""
aiohttp clients module
"""
import sys
from typing import Optional
from typing import Callable

import aiohttp

from qbapi.mapping import DataMapping


class BaseAIOClient:
    """AIOClient"""

    async def make_request(self, session: Callable, url: str, method: str,
                           data: Optional[dict] = None) -> dict:
        """make_request

        :param session:
        :type session: Callable
        :param url:
        :type url: str
        :param str:
        :param data:
        :type data: Optional[dict]
        :rtype: dict
        """

        if method == 'get':
            async with session.get(url) as response:
                return await response.json()
        else:
            async with session.post(url, json=data) as response:
                return await response.json()

    async def request(self, url: str, headers: dict, method: str,
                      data: Optional[dict] = None):
        """request

        :param url:
        :type url: str
        :param headers:
        :type headers: dict
        :param method:
        :type method: str
        """
        async with aiohttp.ClientSession(headers=headers) as session:

            try:
                response = await self.make_request(session, url, method, data)
            except aiohttp.ClientError as error:
                print('Client error: {}'.format(error))
                sys.exit(-1)

            return response

    async def process(self, prod_queue: 'Queue',
                      con_queue: Optional['Queue'] = None) -> dict:
        """process

        :param queue:
        :type queue: 'Queue'
        :rtype: dict
        """
        raise NotImplementedError


class Producer(BaseAIOClient):
    """AIOClient"""

    async def process(self, prod_queue: 'Queue', con_queue: 'Queue') -> dict:
        """process

        :param prod_queue:
        :type prod_queue: 'Queue'
        :param con_queue:
        :type con_queue: 'Queue'
        :rtype: dict
        """
        while True:

            from_api_data, to_api_data, keys_map = await prod_queue.get()

            response = await self.request(*from_api_data.get(), 'get')
            request = await DataMapping(response, keys_map).mapping()

            await con_queue.put((to_api_data, request, ))
            prod_queue.task_done()


class Consumer(BaseAIOClient):
    """AIOClient"""

    async def process(self, con_queue: 'Queue') -> dict:
        """process

        :param con_queue:
        :type con_queue: 'Queue'
        :rtype: dict
        """

        while True:

            to_api_data, request_data = await con_queue.get()

            response = await self.request(
                *to_api_data.get(), 'post', request_data)

            print(response)
            con_queue.task_done()


__ALL__ = [
    'Consumer',
    'Producer'
]
