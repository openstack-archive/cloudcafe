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

from cloudcafe.identity.v3.common.users.models.responses import User


class Mock(object):
    @classmethod
    def _dict_to_obj(cls, data):
        return "mocked stuff"

    @classmethod
    def _xml_ele_to_obj(cls, data):
        return "mocked stuff"


class UserResponseTests(unittest.TestCase):
    """
    Metatests for v3 User response model
    """
    RESPONSES = 'cloudcafe.identity.v3.common.users.models.responses'

    def test_dict_to_obj_data_is_none(self):
        """
        Test to verify User()._dict_to_obj(None) is None
        """
        self.assertEqual(None, User()._dict_to_obj(None))

    @mock.patch(RESPONSES+'.Domain', Mock)
    def test_dict_to_obj(self):
        """
        test to verify User.dict_to_obj() can convert a dictionary
        representation of a User to a User object
        """
        # ARRANGE
        user_dict = {
            'id': 'test_user_id',
            'name': 'test_user_name',
            'default_project_id': 'test_default_project_id',
            'default_region': 'test_default_region',
            'domain': 'test_domain'
        }
        expected_user_resp_obj = User(
            id_='test_user_id',
            name='test_user_name',
            default_project_id='test_default_project_id',
            default_region='test_default_region',
            domain='mocked stuff')
        # ACT
        user_resp_obj = User._dict_to_obj(user_dict)
        # ASSERT
        self.assertEqual(expected_user_resp_obj, user_resp_obj)


if __name__ == '__main__':
    unittest.main()
