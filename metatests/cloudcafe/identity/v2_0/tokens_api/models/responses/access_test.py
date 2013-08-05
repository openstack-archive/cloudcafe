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
    ServiceCatalog, Access, Service, Endpoint, EndpointList, User, Role, \
    RoleList, Token, Tenant


class TestAccess(object):

    @classmethod
    def setup_class(cls):
        cls.access_json_dict = (open(os.path.join(
            os.path.dirname(__file__), "../../data/access.json")).read())
        cls.access_dict = json.loads(cls.access_json_dict).get('access')
        cls.token_dict = cls.access_dict.get('token')
        cls.tenant_dict = cls.token_dict.get('tenant')
        cls.tenant = Tenant(id_=cls.tenant_dict.get('id'),
                            name=cls.tenant_dict.get('name'),
                            enabled=cls.tenant_dict.get('enabled'),
                            description=cls.tenant_dict.get('description'))

        cls.token = Token(id_=cls.token_dict.get('id'),
                          issued_at=cls.token_dict.get('issued_at'),
                          expires=cls.token_dict.get('expires'),
                          tenant=cls.tenant)
        cls.service_catalog_dict = cls.access_dict.get('serviceCatalog')
        cls.user_dict = cls.access_dict.get('user')
        cls.roles_dict = cls.user_dict.get('roles')
        cls.role_dict = cls.roles_dict[0]
        cls.service_dict = cls.service_catalog_dict[0]
        cls.another_service_dict = cls.service_catalog_dict[1]
        cls.endpoint_dict = cls.service_dict.get('endpoints')[0]
        cls.endpoint = Endpoint(id_=cls.endpoint_dict.get('id'),
                                admin_url=cls.endpoint_dict.get('adminURL'),
                                internal_url=cls.endpoint_dict.get(
                                    'internalURL'),
                                public_url=cls.endpoint_dict.get(
                                    'publicURL'),
                                region=cls.endpoint_dict.get('region'))
        cls.region = cls.endpoint_dict.get('region')
        cls.endpoints = EndpointList(endpoints=[cls.endpoint])
        cls.endpoints_links = cls.service_dict.get('endpoints_links')

        cls.role = Role(id_=cls.role_dict.get('id'),
                        name=cls.role_dict.get('name'))

        cls.roles = RoleList(roles=[cls.role])
        cls.roles_links = cls.user_dict.get('roles_links')
        cls.user = User(id_=cls.user_dict.get('id'),
                        name=cls.user_dict.get('name'),
                        username=cls.user_dict.get('username'),
                        roles=cls.roles,
                        roles_links=cls.roles_links)

        cls.metadata_dict = cls.access_dict.get('metadata')
        cls.service_name = cls.service_dict.get('name')
        cls.service = Service(name=cls.service_name,
                              type_=cls.service_dict.get('type'),
                              endpoints=cls.endpoints,
                              endpoint_links=cls.endpoints_links)

        cls.another_service = Service(name=cls.service_name,
                                      type_=cls.another_service_dict.get(
                                          'type'),
                                      endpoints=cls.endpoints,
                                      endpoint_links=cls.endpoints_links)

        cls.services = [Service(name=service_dict.get('name'),
                                type_=service_dict.get('type'),
                                endpoints=EndpointList._list_to_obj(
                                    [service_dict.get('endpoints')[0]]),
                                endpoint_links=service_dict.get(
                                    'endpoints_links'))
                        for service_dict in cls.service_catalog_dict]

        cls.service_catalog = ServiceCatalog(services=[cls.service])
        cls.another_service_catalog = ServiceCatalog(services=cls.services)

        cls.access = Access(metadata=cls.metadata_dict,
                            service_catalog=cls.another_service_catalog,
                            user=cls.user, token=cls.token)

        cls.glance_service = Service(name="Glance")

    def test_get_service(self):
        assert self.service == self.access.get_service(name=self.service_name)
        assert self.access.get_service(name="Glance") is None

    def test_dict_to_obj(self):
        assert self.endpoint == Endpoint._dict_to_obj(self.endpoint_dict)
        assert self.service == Service._dict_to_obj(self.service_dict)
        assert self.user == User._dict_to_obj(self.user_dict)
        assert self.access == Access._dict_to_obj(self.access_dict)
        assert self.token == Token._dict_to_obj(self.token_dict)
        assert self.tenant == Tenant._dict_to_obj(self.tenant_dict)
        assert self.role == Role._dict_to_obj(self.role_dict)

    def test_list_to_obj(self):
        assert self.endpoints == EndpointList._list_to_obj(
            [self.endpoint_dict])
        assert self.service_catalog == ServiceCatalog._list_to_obj(
            [self.service_dict])
        assert self.roles == RoleList._list_to_obj([self.role_dict])

    def test_json_to_obj(self):
        assert self.access == Access._json_to_obj(self.access_json_dict)

    def test_get_endpoint(self):
        assert self.endpoint == self.service.get_endpoint(self.region)
        assert self.service.get_endpoint('non_existing_region') is None
