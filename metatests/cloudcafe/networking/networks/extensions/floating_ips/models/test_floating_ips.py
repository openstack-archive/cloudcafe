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
import ast
import unittest
from uuid import uuid4

from cloudcafe.networking.networks.extensions.floating_ips.constants \
    import FloatingIPStates
from cloudcafe.networking.networks.extensions.floating_ips.models.request \
    import FloatingIPRequest, FloatingIPUpdate
from cloudcafe.networking.networks.extensions.floating_ips.models.response \
    import FloatingIPInfo, FloatingIPInfoList


class CreateFloatingIPAssociation(unittest.TestCase):
    """ Validate the create request model obj_to_json conversion. """

    @classmethod
    def setUpClass(cls):
        tenant_id = uuid4().urn[9:]
        floating_network_id = uuid4().urn[9:]
        port_id = uuid4().urn[9:]
        floating_ip_address = '172.27.58.59'
        fixed_ip_address = '10.1.25.254'

        floating_ip_args = {
            'floating_network_id': floating_network_id,
            'floating_ip_address': floating_ip_address,
            'tenant_id': tenant_id,
            'fixed_ip_address': fixed_ip_address,
            'port_id': port_id,
        }

        cls.floating_ip_obj = FloatingIPRequest(**floating_ip_args)
        cls.expected_json = (
            '{{"{root_tag}": {{"floating_network_id": "{floating_network_id}",'
            '"floating_ip_address": "{floating_ip_address}",'
            '"tenant_id": "{tenant_id}",'
            '"fixed_ip_address": "{fixed_ip_address}",'
            '"port_id": "{port_id}"}}'
            '}}').format(
                root_tag=FloatingIPRequest.ROOT_TAG, **floating_ip_args)

    def test_create_request_obj_to_json_translation(self):
        # Convert both JSON strings into Python dictionaries. Removes any
        # key hashing order dependence
        obj_to_json = ast.literal_eval(
            self.floating_ip_obj._obj_to_json())
        expected_json = ast.literal_eval(self.expected_json)
        self.assertEqual(obj_to_json, expected_json)


class UpdateFloatingIPAssociation(unittest.TestCase):
    """ Validate the update request model obj_to_json conversion. """

    @classmethod
    def setUpClass(cls):

        port_id = uuid4().urn[9:]
        floating_ip_args = {'port_id': port_id}

        cls.floating_ip_obj = FloatingIPUpdate(**floating_ip_args)
        cls.expected_json = (
            '{{"{root_tag}": {{"port_id": "{port_id}"}} }}').format(
                root_tag=FloatingIPRequest.ROOT_TAG, **floating_ip_args)

    def test_update_request_obj_to_json_translation(self):
        # Convert both JSON strings into Python dictionaries. Removes any
        # key hashing order dependence
        obj_to_json = ast.literal_eval(self.floating_ip_obj._obj_to_json())
        expected_json = ast.literal_eval(self.expected_json)
        self.assertEqual(obj_to_json, expected_json)


class FloatingIPInfoListResponse(unittest.TestCase):
    """ Validate the request model list info obj_to_json conversion. """

    MODEL = FloatingIPInfoList
    LIST_ELEMENT_MODEL = FloatingIPInfo
    RESPONSE_FORMAT = 'json'
    NUM_OF_FLIPS = 10

    @classmethod
    def setUpClass(cls):

        cls.expected_response_obj = []
        cls.json_parts = []

        json_part_format = """
        {{
           "id": "{id_}",
           "fixed_ip_address": "{fixed_ip_address}",
           "floating_ip_address": "{floating_ip_address}",
           "floating_network_id": "{floating_network_id}",
           "port_id": "{port_id}",
           "router_id": "{router_id}",
           "status": "{status}",
           "tenant_id": "{tenant_id}"
        }} """

        # Generate FLIP info data and object
        for index in xrange(cls.NUM_OF_FLIPS):
            port_id = uuid4().urn[9:]
            tenant_id = uuid4().urn[9:]
            router_id = uuid4().urn[9:]
            floating_network_id = uuid4().urn[9:]
            id_ = uuid4().urn[9:]
            fixed_ip_address = '10.10.225.254'
            floating_ip_address = '172.27.28.58'
            status = FloatingIPStates.ACTIVE

            floating_ip_args = {
                'tenant_id': tenant_id, 'router_id': router_id, 'id_': id_,
                'fixed_ip_address': fixed_ip_address, 'status': status,
                'floating_ip_address': floating_ip_address, 'port_id': port_id,
                'floating_network_id': floating_network_id,
            }

            cls.expected_response_obj.append(
                cls.LIST_ELEMENT_MODEL(**floating_ip_args))
            cls.json_parts.append(json_part_format.format(**floating_ip_args))

        # Build JSON list structure
        list_body = ','.join(cls.json_parts)
        cls.json_response = '{{ "{root_tag}": [{body}\n    ]\n}}'.format(
            root_tag=cls.MODEL.ROOT_TAG, body=list_body)

    def test_deserialize_flip_info_list_response_into_obj(self):
        response_obj = self.MODEL.deserialize(self.json_response,
                                              self.RESPONSE_FORMAT)
        self.assertEqual(response_obj, self.expected_response_obj)

class FloatingIPInfoResponse(unittest.TestCase):
    """ Validate the info model obj_to_json conversion. """

    MODEL = FloatingIPInfo
    RESPONSE_FORMAT = 'json'

    @classmethod
    def setUpClass(cls):
        port_id = uuid4().urn[9:]
        tenant_id = uuid4().urn[9:]
        router_id = uuid4().urn[9:]
        floating_network_id = uuid4().urn[9:]
        id_ = uuid4().urn[9:]
        fixed_ip_address = '10.10.225.254'
        floating_ip_address = '172.27.28.58'
        status = FloatingIPStates.ACTIVE

        floating_ip_args = {
            'tenant_id': tenant_id, 'router_id': router_id, 'id_': id_,
            'fixed_ip_address': fixed_ip_address, 'status': status,
            'floating_ip_address': floating_ip_address, 'port_id': port_id,
            'floating_network_id': floating_network_id,
        }

        cls.floating_ip_info_obj = cls.MODEL(**floating_ip_args)
        cls.json_response = """
            {{ "{root_tag}":
                {{
                    "id": "{id_}",
                    "fixed_ip_address": "{fixed_ip_address}",
                    "floating_ip_address": "{floating_ip_address}",
                    "floating_network_id": "{floating_network_id}",
                    "port_id": "{port_id}",
                    "router_id": "{router_id}",
                    "status": "{status}",
                    "tenant_id": "{tenant_id}"
                }}
            }}""".format(root_tag=cls.MODEL.ROOT_TAG, **floating_ip_args)

    def test_deserialize_flip_info_response_into_obj(self):
        response_obj = FloatingIPInfo.deserialize(self.json_response,
                                                  self.RESPONSE_FORMAT)

        self.assertEqual(response_obj, self.floating_ip_info_obj)


if __name__ == '__main__':
    unittest.main()
