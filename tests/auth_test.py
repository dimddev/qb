import pytest
import base64
from qbapi.auth import AuthToken
from qbapi.auth import AuthBasic


def test_auth_token():
    """test_auth_token"""
    auth_token = AuthToken('supersecrettoken')
    assert auth_token.get_header() == {'Authorization': 'token supersecrettoken'}

def test_auth_basic():
    password = 'supersecretpassword'
    auth_basic = AuthBasic('supersecretpassword')
    b64pass = base64.b64encode(password.encode('utf-8'))
    assert auth_basic.get_header() == {
        'Authorization': 'Basic {}'.format(b64pass.decode())}
