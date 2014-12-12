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

from cloudcafe.identity.v3.common.tokens.models.requests import (
    Auth, Identity, Token, Scope, Password)


class Mock(object):

    def __init__(cls, **kwargs):
        pass

    @classmethod
    def _obj_to_dict(cls):
        return "mocked stuff"


class AuthRequestTests(unittest.TestCase):
    """
    Metatests for v3 Auth block of request
    """
    ROOT_TAG = 'auth'

    @mock.patch('__main__.Scope', Mock)
    @mock.patch('__main__.Identity', Mock)
    def test_obj_to_dict(self):
        """
        test to verify Auth.obj_to_dict() can convert an Auth object to
        a dictionary
        """
        # ARRANGE
        test_auth_obj = Auth(
            identity=Identity(),
            scope=Scope()
        )
        expected_auth_dict = {
            self.ROOT_TAG: {
                'identity': 'mocked stuff',
                'scope': 'mocked stuff'
            }
        }
        # ACT
        test_auth_dict = test_auth_obj._obj_to_dict()
        # ASSERT
        self.assertEqual(expected_auth_dict, test_auth_dict)


class IdentityRequestTests(unittest.TestCase):
    """
    Metatests for v3 Identity block of request
    """
    REQUESTS = 'cloudcafe.identity.v3.common.tokens.models.requests'

    @mock.patch(REQUESTS+'.Password', Mock)
    @mock.patch(REQUESTS+'.Token', Mock)
    def test_obj_to_dict(self):
        """
        test to verify Identity.obj_to_dict() can convert an Identity object to
        a dictionary
        """
        # ARRANGE
        test_identity_obj = Identity(
            token_id='test_token_id',
            token='test_token',
            methods='test_methods',
            username='test_username',
            password='test_password',
            user_id='test_user_id',
            user_domain_id='test_user_domain_id',
            user_domain_name='test_user_domain_name')

        expected_identity_dict = {
            'methods': 'test_methods',
            'token': 'mocked stuff',
            'password': 'mocked stuff'
        }

        # ACT
        test_identity_dict = test_identity_obj._obj_to_dict()
        # ASSERT
        self.assertEqual(expected_identity_dict, test_identity_dict)


class TokenRequestTests(unittest.TestCase):
    """
    Metatests for v3 token block
    """

    def test_obj_to_dict(self):
        """
        test to verify Token.obj_to_dict() can convert an Token object to
        a dictionary
        """
        # ARRANGE
        test_token_obj = Token(token_id='test_token_id')
        expected_token_dict = {
            'id': 'test_token_id'
        }
        # ACT
        test_token_dict = test_token_obj._obj_to_dict()
        # ASSERT
        self.assertEqual(expected_token_dict, test_token_dict)


class ScopeRequestTests(unittest.TestCase):
    """
    Metatests for v3 scope block
    """
    REQUESTS = 'cloudcafe.identity.v3.common.tokens.models.requests'

    def test_obj_to_dict(self):
        """
        test to verify Scope.obj_to_dict() can convert an Scope object to
        a dictionary
        """
        # ARRANGE
        test_scope_obj = Scope(
            domain_name='test_domain_name',
            domain_id='test_domain_id',
            project_domain_name='test_project_domain_name',
            project_domain_id='test_project_domain_id',
            project_name='test_project_name',
            project_id='test_project_id')

        expected_scope_dict = {
            'domain': {
                'name': 'test_domain_name',
                'id': 'test_domain_id'
            },
            'project': {
                'id': 'test_project_id',
                'name': 'test_project_name',
                'domain': {
                    'id': 'test_project_domain_id',
                    'name': 'test_project_domain_name'
                }

            }
        }
        # ACT
        test_scope_dict = test_scope_obj._obj_to_dict()
        # ASSERT
        self.assertEqual(expected_scope_dict, test_scope_dict)


class PasswordRequestTests(unittest.TestCase):
    """
    Metatests for v3 password block
    """
    ROOT_TAG = 'user'

    def test_obj_to_dict(self):
        """
        test to verify Password.obj_to_dict() can convert
        an Password object to a dictionary
        """
        # ARRANGE
        test_password_obj = Password(
            username='test_username',
            user_id='test_user_id',
            password='test_password',
            user_domain_id='test_user_domain_id',
            user_domain_name='test_user_domain_name')
        expected_password_dict = {
            self.ROOT_TAG: {
                'name': 'test_username',
                'id': 'test_user_id',
                'password': 'test_password',
                'domain': {
                    'id': 'test_user_domain_id',
                    'name': 'test_user_domain_name'
                }
            }
        }
        # ACT
        test_password_dict = test_password_obj._obj_to_dict()
        # ASSERT
        self.assertEqual(expected_password_dict, test_password_dict)


if __name__ == '__main__':
    unittest.main()
