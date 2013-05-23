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

import os
from unittest import TestCase
import json
from cloudcafe.identity.v2_0.tokens_api.models.responses.access import \
    ServiceCatalog, Access, Service, Endpoint, EndpointList, User


class AccessTest(TestCase):
    def setUp(self):
        print os.pardir

        self.access_json_dict = (open(os.path.join(
            os.path.dirname(__file__), "../../data/access.json")).read())
        self.access_dict = json.loads(self.access_json_dict).get('access')
        self.expected_access = Access._dict_to_obj(self.access_dict)

        self.service_name = "Nova"
        self.nova_service = Service(name=self.service_name)
        self.glance_service = Service(name="Glance")
        self.service_catalog = ServiceCatalog(services=[self.nova_service])
        self.access = Access(service_catalog=self.service_catalog)

        self.url = "ADMIN_URL"
        self.region = "REGION"
        self.internal_url = "INTERNAL_URL"
        self.public_url = "PUBLIC_URL"
        self.id = "ID"
        self.endpoint_json_dict = {'adminURL': self.url, 'region': self.region,
                                   'internalURL': self.internal_url,
                                   'id': self.id,
                                   'publicURL': self.public_url}

        self.expected_endpoint = Endpoint(admin_url=self.url,
                                          region=self.region,
                                          internal_url=self.internal_url,
                                          id_=self.id,
                                          public_url=self.public_url)

        self.expected_endpoint_list = EndpointList(
            endpoints=[self.expected_endpoint])

        self.service_json_dict = {'endpoints': [self.endpoint_json_dict],
                                  'endpoints_links': [],
                                  'type': "TYPE", 'name': self.service_name}
        self.expected_service = Service(endpoints=[self.expected_endpoint],
                                        endpoint_links=[],
                                        name=self.service_name,
                                        type_="TYPE")

        self.service_dict_list = [self.service_json_dict]
        self.expected_service_catalog = ServiceCatalog(
            services=[self.expected_service])

        self.user_json_dict = {'id': "1", 'name': "NAME",
                               'username': "USERNAME",
                               'roles': [], 'roles_links': []}
        self.expected_user = User(id_="1", name="NAME",
                                  username="USERNAME",
                                  roles=[], roles_links=[])

    def test_get_service(self):
        assert self.nova_service == self.access.get_service(
            name=self.service_name)
        assert self.access.get_service(name="Glance") is None

    def test_dict_to_obj(self):
        assert self.expected_endpoint == \
            Endpoint._dict_to_obj(self.endpoint_json_dict)
        assert self.expected_service == Service._dict_to_obj(
            self.service_json_dict)
        assert self.expected_user == User._dict_to_obj(self.user_json_dict)

    def test_list_to_obj(self):
        assert self.expected_endpoint_list == \
            EndpointList._list_to_obj([self.endpoint_json_dict])
        assert self.expected_service_catalog == \
            ServiceCatalog._list_to_obj(self.service_dict_list)

    def test_json_to_obj(self):
        assert self.expected_access == Access._json_to_obj(
            self.access_json_dict)
