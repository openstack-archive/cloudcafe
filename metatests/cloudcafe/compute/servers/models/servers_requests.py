"""
Copyright 2013 Rackspace

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

import unittest2 as unittest

from cloudcafe.compute.servers_api.models.requests import CreateServer


class CreateServerJSONDomainTest(object):

    def test_block_device_mapping_json(self):
        block = ('"block_device_mapping": [{"device_name": "vda",'
                 '"delete_on_termination": "0",'
                 '"volume_id": "9f10839f-beff-41f0-a837-8b97bbd33a78"}]')
        block_dict = "".join(block.split())
        self.assertIn(block_dict, self.serialized_request,
                      msg="Block Mapping was not found in serialized request")


class CreateServerObjectJSON(unittest.TestCase, CreateServerJSONDomainTest):

    @classmethod
    def setUpClass(cls):

        block = [{"volume_id": "9f10839f-beff-41f0-a837-8b97bbd33a78",
                  "delete_on_termination": "0", "device_name": "vda"}]

        server_request_object = CreateServer(
            name='cctestserver',
            flavor_ref='2',
            image_ref='sample-image-ref',
            block_device_mapping=block)

        cls.server_request_json = server_request_object.serialize('json')
        cls.serialized_request = "".join(cls.server_request_json.split())
