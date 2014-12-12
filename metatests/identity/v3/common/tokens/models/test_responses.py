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
import json

from cloudcafe.identity.v3.common.tokens.models.responses\
    import AuthResponse, AuthResponseToken


class Mock(object):
    @classmethod
    def _dict_to_obj(cls, data):
        return "mocked stuff"

    @classmethod
    def _xml_ele_to_obj(cls, data):
        return "mocked stuff"


class AuthResponseTests(unittest.TestCase):
    """
    Metatests class for the v3 AuthResponse model
    """

    RESPONSES = 'cloudcafe.identity.v3.common.tokens.models.responses'

    def test_dict_to_obj_data_is_none(self):
        """
        Test to verify AuthResponse()._dict_to_obj(None) is None
        """
        self.assertEqual(None, AuthResponse()._dict_to_obj(None))

    @mock.patch(RESPONSES+'.AuthResponseToken', Mock)
    @mock.patch(RESPONSES+'.Roles', Mock)
    @mock.patch(RESPONSES+'.Catalog', Mock)
    @mock.patch(RESPONSES+'.Project', Mock)
    @mock.patch(RESPONSES+'.User', Mock)
    def test_dict_to_obj(self):
        """
        Test to verify AuthResponse._dict_to_obj() can convert a dictionary
        representation of AuthResponse to an AuthResponse object
        """
        # ARRANGE
        token_dict = {
            'token': 'test_token',
            'roles': 'test_roles',
            'user': 'test_user',
            'catalog': 'test_catalog',
            'issued_at': 'test_issues_at',
            'extras': 'test_extras',
            'methods': 'test_method',
            'project': 'test_project',
            'expires_at': 'test_expires_at'
        }

        expected_obj = AuthResponse(methods="test_method",
                                    roles="mocked stuff",
                                    catalog="mocked stuff",
                                    expires_at="test_expires_at",
                                    project="mocked stuff",
                                    token="mocked stuff",
                                    extras="test_extras",
                                    user="mocked stuff",
                                    issued_at="test_issues_at")
        # ACT
        auth_response_obj = AuthResponse()._dict_to_obj(token_dict)
        # ASSERT
        self.assertEqual(expected_obj, auth_response_obj)

    @mock.patch(RESPONSES+'.AuthResponseToken', Mock)
    @mock.patch(RESPONSES+'.Roles', Mock)
    @mock.patch(RESPONSES+'.Catalog', Mock)
    @mock.patch(RESPONSES+'.Project', Mock)
    @mock.patch(RESPONSES+'.User', Mock)
    def test_json_to_obj(self):
        """
        Test to verify AuthResponse._json_to_obj() can convert a JSON
        representation of AuthResponse to an AuthResponse object
        """
        # ARRANGE
        data = {
            "access": {
                "token": "test_token",
                "roles": "test_roles",
                "user": "test_user",
                "catalog": "test_catalog",
                "issued_at": "test_issued_at",
                "extras": "test_extras",
                "methods": "test_method",
                "project": "test_project",
                "expires_at": "test_expires_at"}
        }

        token_json = json.dumps(data)

        expected_obj = AuthResponse(methods="test_method",
                                    roles="mocked stuff",
                                    catalog="mocked stuff",
                                    expires_at="test_expires_at",
                                    project="mocked stuff",
                                    token="mocked stuff",
                                    extras="test_extras",
                                    user="mocked stuff",
                                    issued_at="test_issued_at")

        # ACT
        auth_response_obj = AuthResponse._json_to_obj(token_json)
        # print auth_response_obj
        # ASSERT
        self.assertEqual(expected_obj, auth_response_obj)


class AuthResponseTokenTests(unittest.TestCase):
    """
    Metatests class for the v3 AuthResponseToken model
    """

    RESPONSES = 'cloudcafe.identity.v3.common.tokens.models.responses'

    def test_dict_to_obj_data_is_none(self):
        """
        Test to verify AuthResponseToken()._dict_to_obj(None) is None
        """
        self.assertEqual(None, AuthResponseToken()._dict_to_obj(None))

    @mock.patch(RESPONSES+'.Tenant', Mock)
    def test_dict_to_obj(self):
        """
        Test to verify AuthResponseToken._dict_to_obj() can convert
        a dictionary representation of AuthResponseToken to
        an AuthResponseToken object
        """
        # ARRANGE
        token_dict = {
            'id': 'test_token_id',
            'expires': 'test_expires',
            'tenant': 'test_tenant'
        }
        expected_obj = AuthResponseToken(
            token_id="test_token_id",
            expires="test_expires",
            tenant="mocked stuff")
        # ACT
        auth_response_token_obj = AuthResponseToken._dict_to_obj(token_dict)
        # ASSERT
        self.assertEqual(expected_obj, auth_response_token_obj)


if __name__ == '__main__':
    unittest.main()
