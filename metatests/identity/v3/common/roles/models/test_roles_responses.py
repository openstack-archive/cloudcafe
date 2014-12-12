"""
Copyright 2014 Rackspace
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import unittest
import mock

from cloudcafe.identity.v3.common.roles.models.responses import Role, Roles


class Mock(object):
    @classmethod
    def _dict_to_obj(cls, data):
        return "mocked stuff"

    @classmethod
    def _xml_ele_to_obj(cls, data):
        return "mocked stuff"


class RoleResponseTests(unittest.TestCase):
    """
    Metatests for v3 Role response model
    """
    def test_dict_to_obj_data_is_none(self):
        """
        Test to verify Role()._dict_to_obj(None) is None
        """
        self.assertEqual(None, Role()._dict_to_obj(None))

    def test_dict_to_obj(self):
        """
        test to verify Role.dict_to_obj() can convert a dictionary
        representation of a Role to a Role object
        """
        # ARRANGE
        role_dict = {
            'id': 'test_role_id',
            'name': 'test_role_name',
            'tenant_id': 'test_tenant_id'
        }
        expected_role_response_obj = Role(id_='test_role_id',
                                          name='test_role_name',
                                          tenant_id='test_tenant_id')
        # ACT
        role_resp_obj = Role._dict_to_obj(role_dict)
        # ASSERT
        self.assertEqual(expected_role_response_obj, role_resp_obj)


class RolesResponseTests(unittest.TestCase):
    """
    Metatests for v3 Roles response model
    """
    RESPONSES = 'cloudcafe.identity.v3.common.roles.models.responses'

    @mock.patch(RESPONSES+'.Role', Mock)
    def test_list_to_obj(self):
        """
        test to verify Role.dict_to_obj() can convert a dictionary
        representation of a Role to a Role object
        """
        # ARRANGE
        roles_list = ['test_role_1', 'test_role_2']
        expected_roles_response_obj = Roles()
        expected_roles_response_obj.append('mocked stuff')
        expected_roles_response_obj.append('mocked stuff')
        # ACT
        roles_resp_obj = Roles._list_to_obj(roles_list)
        # ASSERT
        self.assertEqual(expected_roles_response_obj, roles_resp_obj)


if __name__ == '__main__':
    unittest.main()
