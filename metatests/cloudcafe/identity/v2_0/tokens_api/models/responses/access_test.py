import os
from unittest import TestCase
import json
from cloudcafe.identity.v2_0.tokens_api.models.responses.access import \
    ServiceCatalog, Access, Service, Endpoint, EndpointList, User, Role, RoleList, Token, Tenant


class AccessTest(TestCase):
    def setUp(self):
        self.access_json_dict = open(os.path.join(os.path.dirname(__file__),
                                                  "../../data/access.json")).read()

        self.access_dict = json.loads(self.access_json_dict).get('access')
        self.token_dict = self.access_dict.get('token')
        self.tenant_dict = self.token_dict.get('tenant')
        self.tenant = Tenant(id_=self.tenant_dict.get('id'),
                             name=self.tenant_dict.get('name'),
                             enabled=self.tenant_dict.get('enabled'),
                             description=self.tenant_dict.get('description'))

        self.token = Token(id_=self.token_dict.get('id'),
                           issued_at=self.token_dict.get('issued_at'),
                           expires=self.token_dict.get('expires'),
                           tenant=self.tenant)
        self.service_catalog_dict = self.access_dict.get('serviceCatalog')
        self.user_dict = self.access_dict.get('user')
        self.roles_dict = self.user_dict.get('roles')
        self.role_dict = self.roles_dict[0]
        self.service_dict = self.service_catalog_dict[0]
        self.another_service_dict = self.service_catalog_dict[1]
        self.endpoint_dict = self.service_dict.get('endpoints')[0]
        self.endpoint = Endpoint(id_=self.endpoint_dict.get('id'),
                                 admin_url=self.endpoint_dict.get('adminURL'),
                                 internal_url=self.endpoint_dict.get('internalURL'),
                                 public_url=self.endpoint_dict.get('publicURL'),
                                 region=self.endpoint_dict.get('region'))
        self.region = self.endpoint_dict.get('region')
        self.endpoints = EndpointList(endpoints=[self.endpoint])
        self.endpoints_links = self.service_dict.get('endpoints_links')

        self.role = Role(id_=self.role_dict.get('id'),
                         name=self.role_dict.get('name'))

        self.roles = RoleList(roles=[self.role])
        self.roles_links = self.user_dict.get('roles_links')
        self.user = User(id_=self.user_dict.get('id'),
                         name=self.user_dict.get('name'),
                         username=self.user_dict.get('username'),
                         roles=self.roles,
                         roles_links=self.roles_links)

        self.metadata_dict = self.access_dict.get('metadata')
        self.service_name = self.service_dict.get('name')
        self.service = Service(name=self.service_name,
                               type_=self.service_dict.get('type'),
                               endpoints=self.endpoints,
                               endpoint_links=self.endpoints_links)

        self.another_service = Service(name=self.service_name,
                                       type_=self.another_service_dict.get('type'),
                                       endpoints=self.endpoints,
                                       endpoint_links=self.endpoints_links)

        self.services = [Service(name=service_dict.get('name'),
                                 type_=service_dict.get('type'),
                                 endpoints=EndpointList._list_to_obj([service_dict.get('endpoints')[0]]),
                                 endpoint_links=service_dict.get('endpoints_links'))
                         for service_dict in self.service_catalog_dict]

        self.service_catalog = ServiceCatalog(services=[self.service])
        self.another_service_catalog = ServiceCatalog(services=self.services)

        self.access = Access(metadata=self.metadata_dict,
                             service_catalog=self.another_service_catalog,
                             user=self.user, token=self.token)

        self.glance_service = Service(name="Glance")

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

    def test_list_to_obj(self):
        assert self.endpoints == EndpointList._list_to_obj([self.endpoint_dict])
        assert self.service_catalog == ServiceCatalog._list_to_obj([self.service_dict])
        assert self.roles == RoleList._list_to_obj([self.role_dict])

    def test_json_to_obj(self):
        assert self.access == Access._json_to_obj(self.access_json_dict)

    def test_get_endpoint(self):
        assert self.endpoint == self.service.get_endpoint(self.region)
        assert self.service.get_endpoint('non_existing_region') is None