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

import pytest

from common import get_project_role
from common import has_file_permission
from common import has_permission


class TestPermissions:
    @pytest.mark.asyncio
    async def test_has_permission_true(self, httpx_mock):
        current_identity = {
            'username': 'test',
            'role': 'member',
            'realm_roles': ['test_project-admin'],
        }
        url = 'http://auth/authorize?role=admin&resource=project&zone=core&operation=view&project_code=test_project'
        httpx_mock.add_response(method='GET', json={'result': {'has_permission': True}}, url=url)
        result = await has_permission('http://auth/', 'test_project', 'project', 'core', 'view', current_identity)
        assert result is True

    @pytest.mark.asyncio
    async def test_has_permission_false(self, httpx_mock):
        current_identity = {
            'username': 'test',
            'role': 'member',
            'realm_roles': ['test_project-admin'],
        }
        url = 'http://auth/authorize?role=admin&resource=project&zone=core&operation=view&project_code=test_project'
        httpx_mock.add_response(method='GET', json={'result': {'has_permission': False}}, url=url)
        result = await has_permission('http://auth/', 'test_project', 'project', 'core', 'view', current_identity)
        assert result is False

    @pytest.mark.asyncio
    async def test_has_permission_platform_admin_true(self, httpx_mock):
        current_identity = {
            'username': 'test',
            'role': 'admin',
        }
        url = (
            'http://auth/authorize?role=platform_admin&resource=project&zone=core&operation=view'
            '&project_code=test_project'
        )
        httpx_mock.add_response(method='GET', json={'result': {'has_permission': True}}, url=url)
        result = await has_permission('http://auth/', 'test_project', 'project', 'core', 'view', current_identity)
        assert result is True

    @pytest.mark.asyncio
    async def test_has_permission_no_project_code(self, httpx_mock):
        current_identity = {
            'username': 'test',
            'role': 'member',
            'realm_roles': ['test_project-admin'],
        }
        result = await has_permission('http://auth/', '', 'project', 'core', 'view', current_identity)
        assert result is False

    @pytest.mark.asyncio
    async def test_has_permission_service_error(self, httpx_mock):
        current_identity = {
            'username': 'test',
            'role': 'member',
            'realm_roles': ['test_project-admin'],
        }
        url = 'http://auth/authorize?role=admin&resource=project&zone=core&operation=view&project_code=test_project'
        httpx_mock.add_response(method='GET', json={'result': {'has_permission': True}}, url=url, status_code=500)
        with pytest.raises(Exception):
            await has_permission('http://auth/', 'test_project', 'project', 'core', 'view', current_identity)


class TestFilePermissions:
    @pytest.mark.asyncio
    async def test_has_file_permission_true(self, httpx_mock):
        file_data = {
            'parent_path': 'test',
            'zone': 'core',
            'container_code': 'test_project',
            'container_type': 'project',
        }
        current_identity = {
            'username': 'test',
            'role': 'member',
            'realm_roles': ['test_project-admin'],
        }
        url = (
            'http://auth/authorize?role=admin&resource=file_in_own_namefolder&zone=core&operation=view'
            '&project_code=test_project'
        )
        httpx_mock.add_response(method='GET', json={'result': {'has_permission': True}}, url=url)
        result = await has_file_permission('http://auth/', file_data, 'view', current_identity)
        assert result is True

    @pytest.mark.asyncio
    async def test_has_file_permission_outside_namefolder_true(self, httpx_mock):
        file_data = {
            'parent_path': 'another',
            'zone': 'core',
            'container_code': 'test_project',
            'container_type': 'project',
        }
        current_identity = {
            'username': 'test',
            'role': 'member',
            'realm_roles': ['test_project-admin'],
        }
        url = 'http://auth/authorize?role=admin&resource=file_any&zone=core&operation=view' '&project_code=test_project'
        httpx_mock.add_response(method='GET', json={'result': {'has_permission': False}}, url=url)
        result = await has_file_permission('http://auth/', file_data, 'view', current_identity)
        assert result is False

    @pytest.mark.asyncio
    async def test_has_file_permission_false(self, httpx_mock):
        file_data = {
            'parent_path': 'test',
            'zone': 'core',
            'container_code': 'test_project',
            'container_type': 'project',
        }
        current_identity = {
            'username': 'test',
            'role': 'member',
            'realm_roles': ['test_project-admin'],
        }
        url = (
            'http://auth/authorize?role=admin&resource=file_in_own_namefolder&zone=core&operation=view'
            '&project_code=test_project'
        )
        httpx_mock.add_response(method='GET', json={'result': {'has_permission': False}}, url=url)
        result = await has_file_permission('http://auth/', file_data, 'view', current_identity)
        assert result is False

    @pytest.mark.asyncio
    async def test_has_file_permission_wrong_project(self, httpx_mock):
        file_data = {
            'parent_path': 'test',
            'zone': 'core',
            'container_code': 'test_project2',
            'container_type': 'project',
        }
        current_identity = {
            'username': 'test',
            'role': 'member',
            'realm_roles': ['test_project-admin'],
        }
        result = await has_file_permission('http://auth/', file_data, 'view', current_identity)
        assert result is False

    @pytest.mark.asyncio
    async def test_has_file_permission_wrong_container_type(self, httpx_mock):
        file_data = {
            'parent_path': 'test',
            'zone': 'core',
            'container_code': 'test_project',
            'container_type': 'dataset',
        }
        current_identity = {
            'username': 'test',
            'role': 'member',
            'realm_roles': ['test_project-admin'],
        }
        result = await has_file_permission('http://auth/', file_data, 'view', current_identity)
        assert result is False

    @pytest.mark.asyncio
    async def test_has_file_permission_archived(self, httpx_mock):
        file_data = {
            'archived': True,
            'restore_path': 'test',
            'zone': 'core',
            'container_code': 'test_project',
            'container_type': 'project',
        }
        current_identity = {
            'username': 'test',
            'role': 'member',
            'realm_roles': ['test_project-admin'],
        }
        url = (
            'http://auth/authorize?role=admin&resource=file_in_own_namefolder&zone=core&operation=view'
            '&project_code=test_project'
        )
        httpx_mock.add_response(method='GET', json={'result': {'has_permission': True}}, url=url)
        result = await has_file_permission('http://auth/', file_data, 'view', current_identity)
        assert result is True


class TestGetCurrentRole:
    @pytest.mark.asyncio
    async def test_get_current_role_admin(self, httpx_mock):
        current_identity = {
            'username': 'test',
            'role': 'admin',
            'realm_roles': ['test_project-admin'],
        }
        result = await get_project_role('test_project', current_identity)
        assert result == 'platform_admin'

    @pytest.mark.asyncio
    async def test_get_current_role_member(self, httpx_mock):
        current_identity = {
            'username': 'test',
            'role': 'member',
            'realm_roles': ['test_project-admin'],
        }
        result = await get_project_role('test_project', current_identity)
        assert result == 'admin'
