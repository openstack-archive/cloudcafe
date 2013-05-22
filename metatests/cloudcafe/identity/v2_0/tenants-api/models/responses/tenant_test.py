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

from unittest import TestCase
from cloudcafe.identity.v2_0.tenants_api.models.responses.tenant import \
    Tenant, TenantsLink, Tenants


class TenantTest(TestCase):
    def setUp(self):
        self.tenant_id = "TENANT_ID"
        self.tenant_name = "TENANT_NAME"
        self.tenant_description = "TENANT_DESCRIPTION"
        self.tenant_enabled = False

        self.tenant_dict = {
            "id_": self.tenant_id,
            "name": self.tenant_name,
            "description": self.tenant_description,
            "enabled": self.tenant_enabled}

        self.expected_tenant = Tenant(id_=self.tenant_id,
                                      name=self.tenant_name,
                                      description=self.tenant_description,
                                      enabled=self.tenant_enabled)

        self.tenant_serialized_str = '{"tenant": ' \
                                     '{"id_": "TENANT_ID", ' \
                                     '"enabled": false, ' \
                                     '"name": "TENANT_NAME", ' \
                                     '"description": "TENANT_DESCRIPTION"}}'

        self.expected_tenant_link = TenantsLink(href="HREF", type_="TYPE",
                                                rel="REL")
        self.tenant_list_dict = [self.tenant_dict]
        self.expected_tenants = Tenants(tenants=[self.expected_tenant])

        self.tenants_serialized_str = '{"tenants": ' \
                                      '[{"id_": "TENANT_ID", ' \
                                      '"enabled": false, ' \
                                      '"name": "TENANT_NAME", ' \
                                      '"description": "TENANT_DESCRIPTION"}]}'

    def test_dict_to_obj(self):
        assert self.expected_tenant == Tenant._dict_to_obj(self.tenant_dict)

    def test_json_to_obj(self):
        assert self.expected_tenant == Tenant._json_to_obj(
            self.tenant_serialized_str)
        assert self.expected_tenants == Tenants._json_to_obj(
            self.tenants_serialized_str)

    def test_list_to_obj(self):
        assert self.expected_tenants == Tenants._list_to_obj(
            self.tenant_list_dict)