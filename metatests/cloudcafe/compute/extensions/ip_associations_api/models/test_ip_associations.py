"""
Copyright 2015 Rackspace

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

from cloudcafe.compute.extensions.ip_associations_api.models.request \
    import IPAssociationRequest
from cloudcafe.compute.extensions.ip_associations_api.models.response \
    import IPAssociation, IPAssociations


ERROR_MSG_REQ = ('JSON unexpected IP Association request serialization\n'
                 'Actual Serialization:\n{request}\n'
                 'Expected Serialization:\n{expected}\n')
ERROR_MSG_RESP = ('JSON to Obj response different than expected\n'
                  'Actual Response:\n{response}\n'
                  'Expected Response:\n{expected}\n')


class CreateIPAssociationTest(unittest.TestCase):
    """
    @summary: Test for the IP Associations PUT model object request body
    """
    @classmethod
    def setUpClass(cls):
        cls.ip_association_model = IPAssociationRequest()
        cls.expected_json_output = ('{"ip_association": {}}')

    def test_json_request(self):
        request_body = self.ip_association_model._obj_to_json()
        msg = ERROR_MSG_REQ.format(request=request_body,
                                   expected=self.expected_json_output)
        self.assertEqual(request_body, self.expected_json_output, msg)


class GetIPAssociationTest(unittest.TestCase):
    """
    @sumary: Test for the IP Association GET model object response
    """
    @classmethod
    def setUpClass(cls):
        # Setting the expected response object
        get_attrs = dict(id_='1', address='10.1.1.1')
        cls.expected_response = IPAssociation(**get_attrs)

        # Data simulating the JSON API response
        cls.api_json_resp = ("""
            {"ip_association": {"id": "1", "address": "10.1.1.1"}}""")

    def test_json_response(self):
        response_obj = IPAssociation()._json_to_obj(self.api_json_resp)
        msg = ERROR_MSG_RESP.format(response=response_obj,
                                    expected=self.expected_response)
        self.assertEqual(response_obj, self.expected_response, msg)


class ListIPAssociationsTest(unittest.TestCase):
    """
    @sumary: Test for the IP Associations (List) GET model object response
    """
    @classmethod
    def setUpClass(cls):
        # Setting the expected response object
        get_attrs1 = dict(id_='1', address='10.1.1.1')
        get_attrs2 = dict(id_='2', address='10.1.1.2')
        get_attrs3 = dict(id_='3', address='10.1.1.3')
        ip_association1 = IPAssociation(**get_attrs1)
        ip_association2 = IPAssociation(**get_attrs2)
        ip_association3 = IPAssociation(**get_attrs3)
        cls.expected_response = [ip_association1, ip_association2,
                                 ip_association3]

        # Data simulating the JSON API response
        cls.api_json_resp = ("""
            {"ip_associations": [{"id": "1", "address": "10.1.1.1"},
                                 {"id": "2", "address": "10.1.1.2"},
                                 {"id": "3", "address": "10.1.1.3"}]}
            """)

    def test_json_response(self):
        response_obj = IPAssociations()._json_to_obj(self.api_json_resp)
        msg = ERROR_MSG_RESP.format(response=response_obj,
                                    expected=self.expected_response)
        self.assertEqual(response_obj, self.expected_response, msg)


if __name__ == "__main__":
    unittest.main()
