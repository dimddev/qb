"""
Command line tool
"""
import sys
import asyncio

import trio_click as click

from qbapi.app import spider
from qbapi.common import read_data_file, create_pair_data


@click.command()
@click.option('--from_api', default="https://api.github.com/user",
              help='Fetch API endpoint', type=str,
              show_default=True)
@click.option('--from_cred', help='An API credentials eg. token or password',
              type=str)
@click.option('--from_auth',
              type=click.Choice(['Token', 'Basic'], case_sensitive=False),
              show_default=True, default='Token')
@click.option('--from_map', help="A list of keys used by API as mapping fields",
              multiple=True)
@click.option('--to_api', default="https://targolini.freshdesk.com/api/v2/contacts",
              help='An API create/update endpoint', type=str,
              show_default=True)
@click.option('--to_cred', help='An API credentials eg. token or password',
              type=str)
@click.option('--to_auth',
              type=click.Choice(['Token', 'Basic'], case_sensitive=False),
              show_default=True, default="Basic")
@click.option('--to_map', help="A list of keys used by API as mapping fields",
              multiple=True)
@click.option('--file', help="Path to data file. Check qbapi/config for more info. Use this option alone!")
async def main(**kwargs: dict):
    """main

    :param **kwargs:
    :type **kwargs: dict
    """

    data_file = kwargs.get('file')
    pair_data = read_data_file(data_file)

    if not pair_data:
        kwargs.pop('file')

        if not all([v for _, v in kwargs.items()]):
            print("When --file is not used, all options are required. Try: ./qb.py --help")
            sys.exit(-1)
        pair_data = create_pair_data(kwargs)

    await spider(pair_data)

if __name__ == '__main__':
    LOOP = asyncio.get_event_loop()
    LOOP.run_until_complete(main(_anyio_backend="asyncio"))
