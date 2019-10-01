import base64
import pytest

from qbapi.request import CreateRequest, create_request
from qbapi.auth import AuthToken, AuthBasic
from qbapi.common import read_data_file

PAIR_DATA = read_data_file("./qbapi/config/config.json")

password = 'supersecretpassword:X'
b64pass = base64.b64encode(password.encode('utf-8')).decode()

auth_types = {
    AuthToken: {'Authorization': 'token {}'.format(password)},
    AuthBasic: {'Authorization': 'Basic {}'.format(b64pass)},
}

auth_urls = [
    'https://api.github.com/user',
    'https://targolini.freshdesk.com/api/v2/contacts'
]

mapped_keys = {'name': 'name', 'email': 'email', 'location': 'address'}

def test_create_request_class():
    """test_create_request"""
    x = 0
    for obj, header in auth_types.items():
        create_req = CreateRequest(auth_urls[x], password, obj)

        ret_url, ret_header = create_req.get()

        assert ret_url == auth_urls[x]
        assert ret_header == header

        x += 1


@pytest.mark.asyncio
async def test_create_request():
    """test_create_request"""

    for data in PAIR_DATA:

        from_api, to_api, keys_map = await create_request(data)

        assert isinstance(from_api, CreateRequest)
        assert isinstance(to_api, CreateRequest)

        assert keys_map == mapped_keys

        from_api_url, from_api_header = from_api.get()
        assert 'Authorization' in from_api_header
        assert password in from_api_header['Authorization']
        assert from_api_url == auth_urls[0]

        to_api_url, to_api_header = to_api.get()
        assert 'Authorization' in to_api_header
        assert b64pass in to_api_header['Authorization']
        assert to_api_url == auth_urls[1]
