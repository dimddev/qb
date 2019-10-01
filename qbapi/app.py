"""
Command line tool
"""
import asyncio

from qbapi.request import create_request
from qbapi.services.clients import Producer, Consumer


async def spider(user_data: tuple) -> None:
    """spider

    :param user_data:
    :type user_data: tuple
    :rtype: None
    """

    producer_queue = asyncio.Queue()
    consumer_queue = asyncio.Queue()

    max_workers = 0

    for data in user_data:
        await producer_queue.put(await create_request(data))
        max_workers += 1

    producer_tasks = []
    consumer_tasks = []

    for _ in range(max_workers):

        producer_tasks.append(
            asyncio.create_task(
                Producer().process(producer_queue, consumer_queue)
            )
        )

        consumer_tasks.append(
            asyncio.create_task(
                Consumer().process(consumer_queue)
            )
        )

    await producer_queue.join()
    await consumer_queue.join()

    for i, task in enumerate(producer_tasks):
        task.cancel()
        consumer_tasks[i].cancel()

    await asyncio.gather(*producer_tasks, return_exceptions=True)
    await asyncio.gather(*consumer_tasks, return_exceptions=True)
