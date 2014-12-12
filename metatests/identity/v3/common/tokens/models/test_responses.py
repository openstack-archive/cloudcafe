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
                "token": "mocked_stuff",
                "roles": "mocked_stuff",
                "user": "mocked_stuff",
                "catalog": "mocked_stuff",
                "issued_at": "test_issued_at",
                "extras": "test_extras",
                "methods": "test_method",
                "project": "mocked_stuff",
                "expires_at": "test_expiry"}
        }

        token_json = json.dumps(data)

        expected_obj = AuthResponse(methods="test_method",
                                    roles="mocked stuff",
                                    catalog="mocked stuff",
                                    expires_at="test_expiry",
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

    @mock.patch(RESPONSES+'.Roles', Mock)
    def test_dict_to_obj(self):
        """
        Test to verify AuthResponseToken._dict_to_obj() can convert
        a dictionary representation of AuthResponseToken to
        an AuthResponseToken object
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
        expected_obj = AuthResponseToken(roles="mocked stuff")
        # ACT
        auth_response_token_obj = AuthResponseToken._dict_to_obj(token_dict)
        # ASSERT
        self.assertEqual(expected_obj, auth_response_token_obj)


if __name__ == '__main__':
    unittest.main()
