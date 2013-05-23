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
import json
from cloudcafe.identity.v2_0.tokens_api.models.responses.access import \
    ServiceCatalog, Access, Service, Endpoint, EndpointList, User


class TestAccess:
    @classmethod
    def setup_class(cls):
        cls.access_json_dict = (open(os.path.join(
            os.path.dirname(__file__), "../../data/access.json")).read())
        cls.access_dict = json.loads(cls.access_json_dict).get('access')
        cls.expected_access = Access._dict_to_obj(cls.access_dict)

        cls.service_name = "Nova"
        cls.nova_service = Service(name=cls.service_name)
        cls.glance_service = Service(name="Glance")
        cls.service_catalog = ServiceCatalog(services=[cls.nova_service])
        cls.access = Access(service_catalog=cls.service_catalog)

        cls.url = "ADMIN_URL"
        cls.region = "REGION"
        cls.internal_url = "INTERNAL_URL"
        cls.public_url = "PUBLIC_URL"
        cls.id = "ID"
        cls.endpoint_json_dict = {'adminURL': cls.url, 'region': cls.region,
                                  'internalURL': cls.internal_url,
                                  'id': cls.id,
                                  'publicURL': cls.public_url}

        cls.expected_endpoint = Endpoint(admin_url=cls.url,
                                         region=cls.region,
                                         internal_url=cls.internal_url,
                                         id_=cls.id,
                                         public_url=cls.public_url)

        cls.expected_endpoint_list = EndpointList(
            endpoints=[cls.expected_endpoint])

        cls.service_json_dict = {'endpoints': [cls.endpoint_json_dict],
                                 'endpoints_links': [],
                                 'type': "TYPE", 'name': cls.service_name}
        cls.expected_service = Service(endpoints=[cls.expected_endpoint],
                                       endpoint_links=[],
                                       name=cls.service_name,
                                       type_="TYPE")

        cls.service_dict_list = [cls.service_json_dict]
        cls.expected_service_catalog = ServiceCatalog(
            services=[cls.expected_service])

        cls.user_json_dict = {'id': "1", 'name': "NAME",
                              'username': "USERNAME",
                              'roles': [], 'roles_links': []}
        cls.expected_user = User(id_="1", name="NAME",
                                 username="USERNAME",
                                 roles=[], roles_links=[])

    def test_get_service(self):
        assert self.nova_service == self.access.get_service(
            name=self.service_name)
        assert self.access.get_service(name="Glance") is None

    def test_dict_to_obj(self):
        assert self.expected_endpoint == (Endpoint._dict_to_obj(
            self.endpoint_json_dict))
        assert self.expected_service == Service._dict_to_obj(
            self.service_json_dict)
        assert self.expected_user == User._dict_to_obj(self.user_json_dict)

    def test_list_to_obj(self):
        assert self.expected_endpoint_list == (EndpointList._list_to_obj(
            [self.endpoint_json_dict]))
        assert self.expected_service_catalog == (ServiceCatalog._list_to_obj(
            self.service_dict_list))

    def test_json_to_obj(self):
        assert self.expected_access == Access._json_to_obj(
            self.access_json_dict)
