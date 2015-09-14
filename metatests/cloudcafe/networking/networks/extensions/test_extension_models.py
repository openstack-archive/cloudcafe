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

import cloudcafe.networking.networks.extensions.model as ext_models


class ValidateExtensionEntries(unittest.TestCase):
    """
    This test validates the model generated from a Neutron Extensions query.
    These tests only verify the JSON-to-Obj translation, since there is no
    request (POST/PUT/DELETE) aspect to the API.
    """

    MODEL = ext_models.NeutronExtensions
    LIST_ELEMENT_MODEL = ext_models.NeutronExtension
    RESPONSE_FORMAT = 'json'
    NUM_OF_EXTENSIONS = 10

    @classmethod
    def setUpClass(cls):
        cls.expected_response_obj = []
        cls.json_parts = []

        json_format = """
        {{
            "updated": "{updated}",
            "name": "{name}",
            "links": {links},
            "namespace": "{namespace}",
            "alias": "{alias}",
            "description": "{description}"
        }} """


        data_name = 'test_extension_{0}'
        namespace = 'namespace_link_{0}'
        for index in xrange(cls.NUM_OF_EXTENSIONS):

            data = {'updated': "Timestamp goes here",
                    'name': data_name.format(index),
                    'links': [],
                    'namespace': namespace.format(index),
                    'alias': data_name.format(index),
                    'description': 'A brief description of the extension'}

            cls.expected_response_obj.append(cls.LIST_ELEMENT_MODEL(**data))
            cls.json_parts.append(json_format.format(**data))

        list_body = ','.join(cls.json_parts)
        cls.json_response = '{{ "{root_tag}": [{body}\n    ]\n}}'.format(
            root_tag=cls.MODEL.ROOT_TAG, body=list_body)

    def test_deserialize_extension_list_response_into_obj(self):
        """ Deserialize a JSON response into an NeutronExtensions obj """
        response_obj = self.MODEL.deserialize(
            self.json_response, self.RESPONSE_FORMAT)
        self.assertEqual(response_obj, self.expected_response_obj)
