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
from httpretty import HTTPretty
from cloudcafe.identity.v2_0.tenants_api.client import TenantsAPI_Client

IDENTITY_ENDPOINT_URL = "http://localhost:5000"


class TenantsClientTest(TestCase):
    def setUp(self):
        self.url = IDENTITY_ENDPOINT_URL
        self.serialize_format = "json"
        self.deserialize_format = "json"
        self.auth_token = "AUTH_TOKEN"

        self.tenant_api_client = TenantsAPI_Client(
            url=self.url,
            auth_token=self.auth_token,
            serialize_format=self.serialize_format,
            deserialize_format=self.deserialize_format)

        self.tenant_id = "TENANT_ID"
        self.tenants_url = "{0}/v2.0/tenants".format(self.url)
        self.tenant_url = "{0}/v2.0/tenants/{1}".format(self.url,
                                                        self.tenant_id)
        self.user_id = "USER_ID"
        self.users_url = "{0}/users".format(self.tenant_url)
        self.user_role_url = "{0}/{1}/roles".format(self.users_url,
                                                    self.user_id)

        HTTPretty.enable()

    def test_list_tenants(self):
        HTTPretty.register_uri(HTTPretty.GET, self.tenants_url,
                               body=
                               self._build_list_tenants_expected_response())

        actual_response = self.tenant_api_client.list_tenants()
        self._build_assertions(actual_response, self.tenants_url)

    def test_get_tenant(self):
        HTTPretty.register_uri(HTTPretty.GET, self.tenant_url,
                               body=self._build_get_tenant_expected_response())

        actual_response = self.tenant_api_client.get_tenant(
            tenant_id=self.tenant_id)
        self._build_assertions(actual_response, self.tenant_url)

    def test_create_tenant(self):
        HTTPretty.register_uri(HTTPretty.POST, self.tenants_url)

        actual_response = self.tenant_api_client.create_tenant(name="Admin")
        self._build_assertions(actual_response, self.tenants_url)

    def test_update_tenant(self):
        HTTPretty.register_uri(HTTPretty.PUT, self.tenant_url)

        actual_response = self.tenant_api_client.update_tenant(
            tenant_id=self.tenant_id)
        self._build_assertions(actual_response, self.tenant_url)

    def test_delete_tenant(self):
        HTTPretty.register_uri(HTTPretty.DELETE, self.tenant_url)

        actual_response = self.tenant_api_client.delete_tenant(
            tenant_id=self.tenant_id)
        self._build_assertions(actual_response, self.tenant_url)

    def test_create_user_for_tenant(self):
        HTTPretty.register_uri(HTTPretty.POST, self.users_url)

        actual_response = self.tenant_api_client.create_user_for_a_tenant(
            name="Admin", tenant_id=self.tenant_id)
        self._build_assertions(actual_response, self.users_url)

    def test_get_users_for_tenant(self):
        HTTPretty.register_uri(HTTPretty.GET, self.users_url,
                               body=self._build_list_of_users_for_tenant())

        actual_response = self.tenant_api_client.get_users_for_tenant(
            tenant_id=self.tenant_id)
        self._build_assertions(actual_response, self.users_url)

    def test_create_role_for_tenant_user(self):
        HTTPretty.register_uri(HTTPretty.POST, self.user_role_url)

        actual_response = self.tenant_api_client.create_role_for_tenant_user(
            name="Admin", user_id=self.user_id, tenant_id=self.tenant_id)
        self._build_assertions(actual_response, self.user_role_url)

    def test_get_users_roles_for_tenant(self):
        url = "{0}/{1}/roles".format(self.users_url, self.user_id)
        HTTPretty.register_uri(HTTPretty.GET, url,
                               body=self._build_list_of_roles_for_tenant())

        actual_response = self.tenant_api_client.get_users_roles_on_tenant(
            tenant_id=self.tenant_id,
            user_id=self.user_id)
        self._build_assertions(actual_response, url)

    def _build_assertions(self, actual_response, url):
        assert HTTPretty.last_request.headers['Content-Type'] == \
            'application/{0}'.format(self.serialize_format)
        assert HTTPretty.last_request.headers['Accept'] == \
            'application/{0}'.format(self.serialize_format)
        assert HTTPretty.last_request.headers[
            'X-Auth-Token'] == self.auth_token
        assert 200 == actual_response.status_code
        assert url == actual_response.url

    def _build_list_tenants_expected_response(self):
        return [{"tenants": {"enabled": True,
                             "description": "None",
                             "name": "customer-x",
                             "id": "1"}}]

    def _build_get_tenant_expected_response(self):
        return {"tenant": {"enabled": True,
                           "description": "None",
                           "name": "customer-x",
                           "id": "1"}}

    def _build_list_of_users_for_tenant(self):
        return {"users": [{"name": "user_name",
                           "id": "user_id",
                           "enabled": True,
                           "email": "user_email"}]}

    def _build_list_of_roles_for_tenant(self):
        return {"roles": [{"id": "3",
                           "name": "Member"}]}
