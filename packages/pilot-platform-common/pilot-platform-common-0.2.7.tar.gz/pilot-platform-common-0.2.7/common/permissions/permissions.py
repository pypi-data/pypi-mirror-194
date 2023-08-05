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

from httpx import AsyncClient

from common import LoggerFactory

logger = LoggerFactory('common_permissions').get_logger()


async def has_permission(
    auth_url: str, project_code: str, resource: str, zone: str, operation: str, current_identity: str
):
    if current_identity['role'] == 'admin':
        role = 'platform_admin'
    else:
        if not project_code:
            logger.info('No project code and not a platform admin, permission denied')
            return False
        role = await get_project_role(project_code, current_identity)
        if not role:
            logger.info('Unable to get project role in permissions check, user might not belong to project')
            return False

    try:
        payload = {
            'role': role,
            'resource': resource,
            'zone': zone,
            'operation': operation,
            'project_code': project_code,
        }
        async with AsyncClient(timeout=15) as client:
            response = await client.get(auth_url + 'authorize', params=payload)
        if response.status_code != 200:
            error_msg = f'Error calling authorize API - {response.json()}'
            logger.info(error_msg)
            raise Exception(error_msg)
        if response.json()['result'].get('has_permission'):
            return True
        return False
    except Exception as e:
        error_msg = str(e)
        logger.info(f'Exception on authorize call: {error_msg}')
        raise Exception(f'Error calling authorize API - {error_msg}')


async def get_project_role(project_code, current_identity):
    role = None
    if current_identity['role'] == 'admin':
        role = 'platform_admin'
    else:
        possible_roles = [project_code + '-' + i for i in ['admin', 'contributor', 'collaborator']]
        for realm_role in current_identity['realm_roles']:
            # if this is a role for the correct project
            if realm_role in possible_roles:
                role = realm_role.replace(project_code + '-', '')
    return role


async def has_file_permission(auth_url, file_entity: dict, operation: str, current_identity: dict) -> bool:
    if file_entity['container_type'] != 'project':
        logger.info('Unsupport container type, permission denied')
        return False
    project_code = file_entity['container_code']
    username = current_identity['username']

    zone = 'greenroom' if file_entity['zone'] == 0 else 'core'

    if not file_entity.get('archived'):
        path_for_permissions = 'parent_path'
    else:
        path_for_permissions = 'restore_path'
    root_folder = file_entity[path_for_permissions].split('/')[0]

    if root_folder != username:
        if not await has_permission(auth_url, project_code, 'file_any', zone, operation, current_identity):
            return False
    else:
        if not await has_permission(
            auth_url, project_code, 'file_in_own_namefolder', zone, operation, current_identity
        ):
            return False
    return True
