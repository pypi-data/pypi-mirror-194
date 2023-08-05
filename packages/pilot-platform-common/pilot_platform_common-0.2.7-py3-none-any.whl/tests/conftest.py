# Copyright (C) 2022 Indoc Research
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import asyncio
import time
from uuid import uuid4

import httpx
import jwt
import pytest
import pytest_asyncio
from cryptography.hazmat.primitives.asymmetric import rsa
from dicttoxml import dicttoxml
from starlette.datastructures import Headers
from starlette.requests import Request
from testcontainers.redis import RedisContainer

PROJECT_URL = 'http://project'

PROJECT_ID = str(uuid4())

PROJECT_DATA = {
    'id': PROJECT_ID,
    'code': 'unittestproject',
    'description': 'Test',
    'name': 'Unit Test Project',
    'tags': ['tag1', 'tag2'],
    'system_tags': ['system'],
}

PROJECT_CREDENTIALS = {
    'AccessKeyId': 'test',
    'SecretAccessKey': 'test',
    'SessionToken': 'test',
}


@pytest_asyncio.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
    asyncio.set_event_loop_policy(None)


@pytest.fixture
def mock_get_by_code(httpx_mock):
    code = PROJECT_DATA['code']
    httpx_mock.add_response(
        method='GET',
        url=PROJECT_URL + f'/v1/projects/{code}',
        json=PROJECT_DATA,
        status_code=200,
    )


@pytest.fixture
def mock_get_by_id(httpx_mock):
    httpx_mock.add_response(
        method='GET',
        url=PROJECT_URL + f'/v1/projects/{PROJECT_ID}',
        json=PROJECT_DATA,
        status_code=200,
    )


@pytest.fixture
def mock_post_by_token(httpx_mock):
    url = httpx.URL(
        PROJECT_URL,
        params={
            'Action': 'AssumeRoleWithWebIdentity',
            'WebIdentityToken': 'test',
            'Version': '2011-06-15',
            'DurationSeconds': 86000,
        },
    )
    xml = dicttoxml(
        {
            'AssumeRoleWithWebIdentityResponse': {
                'AssumeRoleWithWebIdentityResult': {'Credentials': PROJECT_CREDENTIALS}
            }
        },
        attr_type=False,
        root=False,
    ).decode('utf-8')
    httpx_mock.add_response(method='POST', url=url, status_code=200, text=xml)


@pytest.fixture(scope='session', autouse=True)
def redis():
    with RedisContainer('redis:latest') as redis:
        host = redis.get_container_host_ip()
        port = redis.get_exposed_port(redis.port_to_expose)
        redis.url = f'redis://{host}:{port}'
        yield redis


def get_mock_jwt_payload(platform_role: str, project_role: str = '', project_code: str = '', expired: bool = False):
    if platform_role == 'admin':
        roles = ['platform-admin']
    else:
        roles = [f'{project_code}-{project_role}']
    current_time = time.time() - 240 if expired else time.time()
    return {
        'exp': current_time + 240,
        'iat': current_time - 60,
        'aud': 'account',
        'sub': platform_role,
        'typ': 'Bearer',
        'acr': '1',
        'realm_access': {'roles': roles},
        'resource_access': {'account': {'roles': roles}},
        'email_verified': True,
        'name': 'test test',
        'preferred_username': 'test',
        'given_name': 'test',
        'family_name': 'test',
        'email': 'test@test.com',
        'group': roles,
    }


@pytest.fixture
def mock_rsa_keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    yield {'private_key': private_key, 'public_key': public_key}


@pytest.fixture
def mock_jwt_admin(mock_rsa_keys):
    payload = get_mock_jwt_payload(platform_role='admin')
    token = jwt.encode(payload=payload, key=mock_rsa_keys['private_key'], algorithm='RS256')
    yield {'private_key': mock_rsa_keys['private_key'], 'public_key': mock_rsa_keys['public_key'], 'token': token}


@pytest.fixture
def mock_jwt_admin_expired(mock_rsa_keys):
    payload = get_mock_jwt_payload(platform_role='admin', expired=True)
    token = jwt.encode(payload=payload, key=mock_rsa_keys['private_key'], algorithm='RS256')
    yield {'private_key': mock_rsa_keys['private_key'], 'public_key': mock_rsa_keys['public_key'], 'token': token}


@pytest.fixture
def mock_jwt_contributor(mock_rsa_keys):
    payload = get_mock_jwt_payload(platform_role='member', project_role='contributor', project_code='testproject')
    token = jwt.encode(payload=payload, key=mock_rsa_keys['private_key'], algorithm='RS256')
    yield {'private_key': mock_rsa_keys['private_key'], 'public_key': mock_rsa_keys['public_key'], 'token': token}


@pytest.fixture
def mock_jwt_collaborator(mock_rsa_keys):
    payload = get_mock_jwt_payload(platform_role='member', project_role='collaborator', project_code='testproject')
    token = jwt.encode(payload=payload, key=mock_rsa_keys['private_key'], algorithm='RS256')
    yield {'private_key': mock_rsa_keys['private_key'], 'public_key': mock_rsa_keys['public_key'], 'token': token}


@pytest.fixture
def mock_get_user_from_auth(httpx_mock):
    response = {
        'result': {
            'id': '44c756a8-94f9-46df-970e-7f6be0f876ad',
            'createdTimestamp': 1665685498762,
            'username': 'test',
            'enabled': True,
            'totp': False,
            'emailVerified': False,
            'email': 'test@test.com',
            'federationLink': '6659269c-3425-4009-bc09-e10319eb22ad',
            'attributes': {
                'LDAP_ENTRY_DN': 'uid=test,cn=users,cn=accounts,dc=example,dc=org',
                'createTimestamp': '20221013182444Z',
                'modifyTimestamp': '20221013182444Z',
                'LDAP_ID': 'test',
                'status': 'active',
            },
            'disableableCredentialTypes': [],
            'requiredActions': [],
            'notBefore': 0,
            'access': {
                'manageGroupMembership': True,
                'view': True,
                'mapRoles': True,
                'impersonate': False,
                'manage': True,
            },
            'first_name': 'test',
            'last_name': 'test',
            'name': 'test',
            'role': 'member',
        }
    }
    httpx_mock.add_response(
        method='GET',
        url='http://AUTH_SERVICE/v1/admin/user?username=test&exact=true',
        json=response,
        status_code=200,
    )


def build_starlette_request(
    method: str = 'GET',
    server: str = 'www.example.com',
    path: str = '/',
    headers: dict = None,
    body: str = None,
) -> Request:
    if headers is None:
        headers = {}
    request = Request(
        {
            'type': 'http',
            'path': path,
            'headers': Headers(headers).raw,
            'http_version': '1.1',
            'method': method,
            'scheme': 'https',
            'client': ('127.0.0.1', 8080),
            'server': (server, 443),
        }
    )
    if body:

        async def request_body():
            return body

        request.body = request_body
    return request


@pytest.fixture
def mock_request_no_headers():
    yield build_starlette_request()


@pytest.fixture
def mock_request_authorization():
    yield build_starlette_request(headers={'Authorization': 'Bearer test_token'})


@pytest.fixture
def mock_request_cookie_with_spaces():
    yield build_starlette_request(headers={'cookie': 'INGRESS_COOKIE=test; AUTH=test_token; OTHER=test_2'})


@pytest.fixture
def mock_request_cookie_no_spaces():
    yield build_starlette_request(headers={'cookie': 'INGRESS_COOKIE=test;AUTH=test_token;OTHER=test_2'})
