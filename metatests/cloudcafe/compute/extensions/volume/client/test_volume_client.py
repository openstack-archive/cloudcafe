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

from httpretty import HTTPretty
from cloudcafe.compute.extensions.volumes_api.client import VolumeClient
from cloudcafe.compute.extensions.volumes_api.models.requests import CreateVolume

from metatests.cloudcafe.compute.extensions.volume.client.responses import VolumeMockResponse
from metatests.cloudcafe.compute.fixtures import ClientTestFixture


class VolumeClientTest(ClientTestFixture):

    @classmethod
    def setUpClass(cls):
        super(VolumeClientTest, cls).setUpClass()
        cls.volume_client = VolumeClient(
            url=cls.COMPUTE_API_ENDPOINT,
            auth_token=cls.AUTH_TOKEN,
            serialize_format=cls.DESERIALIZER_FORMAT,
            deserialize_format=cls.DESERIALIZER_FORMAT)
        cls.volume_uri = "{0}/os-volumes".format( cls.COMPUTE_API_ENDPOINT)
        cls.mock_response = VolumeMockResponse(cls.DESERIALIZER_FORMAT)

    def test_create_volume(self):
        HTTPretty.register_uri(HTTPretty.POST, self.volume_uri,
                               body=self.mock_response.create_volume(), status=201)
        request_args = {"display_name": "vol-001", "display_description": "Another volume.",
                         "size": "30", "volume_type": "289da7f8-6440-407c-9fb4-7db01ec49164",
                         "metadata": {"contents": "junk"}, "availability_zone": "us-east1"}
        response = self.volume_client.create_volume(**request_args)
        expected_request_body=CreateVolume(**request_args).serialize(self.SERIALIZER_FORMAT)
        self.assertEqual(201, response.status_code)
        self.assertEqual(self.mock_response.create_volume(), response.content)
        self.assertEqual(HTTPretty.last_request.body, expected_request_body)

