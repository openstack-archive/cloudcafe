import json
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
            "id": self.tenant_id,
            "name": self.tenant_name,
            "description": self.tenant_description,
            "enabled": self.tenant_enabled}

        self.href = "HREF"
        self.type = "TYPE"
        self.rel = "REL"
        self.tenants_link_dict = {"href": self.href,
                                  "type": self.type,
                                  "rel": self.rel}

        self.expected_tenant = Tenant(id_=self.tenant_id,
                                      name=self.tenant_name,
                                      description=self.tenant_description,
                                      enabled=self.tenant_enabled)

        self.tenant_serialized_str = '{"tenant": ' \
                                     '{"id": "TENANT_ID", ' \
                                     '"enabled": false, ' \
                                     '"name": "TENANT_NAME", ' \
                                     '"description": "TENANT_DESCRIPTION"}}'

        self.expected_tenant_link = TenantsLink(href=self.href,
                                                type_=self.type,
                                                rel=self.rel)
        self.tenant_list_dict = [self.tenant_dict]
        self.expected_tenants = Tenants(tenants=[self.expected_tenant])

        self.tenants_serialized_str = '{"tenants": ' \
                                      '[{"id": "TENANT_ID", ' \
                                      '"enabled": false, ' \
                                      '"name": "TENANT_NAME", ' \
                                      '"description": "TENANT_DESCRIPTION"}]}'
        self.expected_tenant_json = json.dumps({"tenant": self.tenant_dict})
        self.expected_tenants_link_json = \
            json.dumps({"tenantsLink": self.tenants_link_dict})

    def test_dict_to_obj(self):
        assert self.expected_tenant == Tenant._dict_to_obj(self.tenant_dict)
        assert self.expected_tenant_link == TenantsLink._dict_to_obj(
            self.tenants_link_dict)

    def test_json_to_obj(self):
        assert self.expected_tenant == Tenant._json_to_obj(
            self.tenant_serialized_str)
        assert self.expected_tenants == Tenants._json_to_obj(
            self.tenants_serialized_str)

    def test_list_to_obj(self):
        assert self.expected_tenants == Tenants._list_to_obj(
            self.tenant_list_dict)

    def test_ojb_to_json(self):
        assert self.expected_tenant_json == self.expected_tenant._obj_to_json()
        assert self.expected_tenants_link_json == \
            self.expected_tenant_link._obj_to_json()
