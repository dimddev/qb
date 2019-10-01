from pathlib import Path
import json
import asyncio
import pytest

from aioresponses import aioresponses

from qbapi.services.clients import BaseAIOClient
from qbapi.services.clients import Producer, Consumer
from qbapi.mapping import DataMapping
from qbapi.request import create_request
from qbapi.common import read_data_file


from tests.fixtures import git_response, fresh_response

BASE = BaseAIOClient()


@pytest.mark.asyncio
async def test_process():
    """test_process"""
    fake_queue = []
    with pytest.raises(NotImplementedError):
        await BASE.process(fake_queue)


@pytest.mark.asyncio
async def test_producer_consumer_process():
    """test_producer_process"""
    PRODQ = asyncio.Queue()
    CONSQ = asyncio.Queue()

    data_f = read_data_file("./qbapi/config/config.json")

    for data in data_f:
        await PRODQ.put(await create_request(data))

    assert PRODQ.qsize() == 1

    with aioresponses() as mocked:
        # producer request
        mocked.get(
            'https://api.github.com/user',
            payload=git_response
        )

        producer = Producer()
        prod = asyncio.create_task(producer.process(PRODQ, CONSQ))

        await PRODQ.join()
        assert PRODQ.qsize() == 0

        prod.cancel()

    with aioresponses() as mocked:
        # consumer request
        mocked.post(
            'https://targolini.freshdesk.com/api/v2/contacts',
            payload=fresh_response,
            body={'name': 'Di Mita Hakini', 'email': 'targolini@gmail.com', 'address': 'Sofia'}
        )

        assert CONSQ.qsize() == 1

        consumer = Consumer()
        cons = asyncio.create_task(consumer.process(CONSQ))

        await CONSQ.join()
        assert CONSQ.qsize() == 0

        cons.cancel()


@pytest.mark.asyncio
async def test_data_mapping():
    """test_data_mapping"""

    keys_map = {'login': 'name', 'location': 'address'}
    bad_names = {'dasdkasjd': 'dada120', 'qwe': 'asd'}

    mapped_keys = {'name': 'dimddev', 'address': 'Sofia'}

    data_m = DataMapping(git_response, keys_map)
    assert await data_m.mapping() == mapped_keys

    data_m = DataMapping(git_response, bad_names)
    assert await data_m.mapping() == {}
