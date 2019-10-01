"""
Common functions
"""

import json
from pathlib import Path


def read_data_file(data_file: str) -> zip:
    """read_data_file

    :param data_file:
    :type data_file: str
    :rtype: zip
    """
    if data_file and Path(data_file).exists():
        with open(data_file) as fd:
            pair_data = json.load(fd)
        print(pair_data)
        return zip(pair_data.get('from_api'), pair_data.get('to_api'))
    return False

def create_pair_data(kwargs: dict) -> zip:
    """create_pair_data

    :param kwargs:
    :type kwargs: dict
    :rtype: zip
    """

    from_data = ([kwargs.get('from_api'), kwargs.get('from_cred'),
                  kwargs.get('from_auth'), kwargs.get('from_map')], )

    to_data = ([kwargs.get('to_api'), kwargs.get('to_cred'),
                kwargs.get('to_auth'), kwargs.get('to_map')], )

    return zip(from_data, to_data)
