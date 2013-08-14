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
from cloudcafe.identity.v2_0.tenants_api.client import TenantsAPI_Client

IDENTITY_ENDPOINT_URL = "http://localhost:5000"


class TestTenantsClient(object):
    @classmethod
    def setup_class(cls):
        cls.url = IDENTITY_ENDPOINT_URL
        cls.serialize_format = "json"
        cls.deserialize_format = "json"
        cls.auth_token = "AUTH_TOKEN"
        cls.admin_extensions = "OS-KSADM"

        cls.tenant_api_client = TenantsAPI_Client(
            url=cls.url,
            auth_token=cls.auth_token,
            serialize_format=cls.serialize_format,
            deserialize_format=cls.deserialize_format)

        cls.tenant_id = "TENANT_ID"
        cls.tenants_url = "{0}/v2.0/tenants".format(cls.url)
        cls.tenant_url = "{0}/v2.0/tenants/{1}".format(cls.url,
                                                       cls.tenant_id)
        cls.user_id = "USER_ID"
        cls.users_url = "{0}/v2.0/users".format(cls.url)
        cls.user_url = "{0}/{1}".format(cls.users_url, cls.user_id)
        cls.tenant_users_url = "{0}/users".format(cls.tenant_url)
        cls.user_role_url = "{0}/{1}/roles".format(cls.tenant_users_url,
                                                   cls.user_id)
        cls.role_id = "ROLE_ID"
        cls.tenant_user_role_url = "{0}/{1}/{2}".format(cls.user_role_url,
                                                        cls.admin_extensions,
                                                        cls.role_id)

        cls.service_id = "SERVICE_ID"
        cls.services_url = "{0}/v2.0/{1}/services".format(cls.url,
                                                          cls.admin_extensions)
        cls.service_url = "{0}/v2.0/{1}/services/{2}".format(
            cls.url,
            cls.admin_extensions,
            cls.service_id)

        HTTPretty.enable()

    @classmethod
    def teardown_class(cls):
        HTTPretty.disable()

    def test_list_tenants(self):
        HTTPretty.register_uri(
            HTTPretty.GET,
            self.tenants_url,
            body=self._build_list_tenants_expected_response())

        actual_response = self.tenant_api_client.list_tenants()
        self._build_assertions(actual_response, self.tenants_url)

    def test_get_tenant(self):
        HTTPretty.register_uri(HTTPretty.GET,
                               self.tenant_url,
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

    def test_list_users(self):
        HTTPretty.register_uri(
            HTTPretty.GET,
            self.users_url,
            body=self._build_list_users_expected_response())

        actual_response = self.tenant_api_client.list_users()
        self._build_assertions(actual_response, self.users_url)

    def test_get_user(self):
        HTTPretty.register_uri(HTTPretty.GET,
                               self.user_url,
                               body=self._build_get_user_expected_response())

        actual_response = self.tenant_api_client.get_user(user_id=self.user_id)
        self._build_assertions(actual_response, self.user_url)

    def test_create_user_for_tenant(self):
        url = "{0}/v2.0/users".format(self.url)
        HTTPretty.register_uri(HTTPretty.POST, url)

        actual_response = self.tenant_api_client.create_user_for_a_tenant(
            name="Admin", tenant_id=self.tenant_id)
        self._build_assertions(actual_response, url)

    def test_update_user(self):
        HTTPretty.register_uri(HTTPretty.PUT, self.user_url)

        actual_response = self.tenant_api_client.update_user(
            user_id=self.user_id)
        self._build_assertions(actual_response, self.user_url)

    def test_delete_user(self):
        HTTPretty.register_uri(HTTPretty.DELETE, self.user_url)

        actual_response = self.tenant_api_client.delete_user(
            user_id=self.user_id)
        self._build_assertions(actual_response, self.user_url)

    def test_get_users_for_tenant(self):
        HTTPretty.register_uri(HTTPretty.GET,
                               self.tenant_users_url,
                               body=self._build_list_of_users_for_tenant())

        actual_response = self.tenant_api_client.get_users_for_tenant(
            tenant_id=self.tenant_id)
        self._build_assertions(actual_response, self.tenant_users_url)

    def test_assign_role_to_tenant_user(self):
        HTTPretty.register_uri(HTTPretty.PUT, self.tenant_user_role_url)

        actual_response = self.tenant_api_client.assign_role_to_tenant_user(
            name="Admin",
            user_id=self.user_id,
            tenant_id=self.tenant_id,
            role_id=self.role_id)
        self._build_assertions(actual_response, self.tenant_user_role_url)

    def test_get_users_roles_for_tenant(self):
        HTTPretty.register_uri(HTTPretty.GET,
                               self.user_role_url,
                               body=self._build_list_of_roles_for_tenant())

        actual_response = self.tenant_api_client.get_users_roles_on_tenant(
            tenant_id=self.tenant_id,
            user_id=self.user_id)
        self._build_assertions(actual_response, self.user_role_url)

    def test_remove_role_of_tenant_user(self):
        HTTPretty.register_uri(HTTPretty.DELETE, self.tenant_user_role_url)

        actual_response = self.tenant_api_client.remove_role_of_tenant_user(
            tenant_id=self.tenant_id,
            user_id=self.user_id,
            role_id=self.role_id)
        self._build_assertions(actual_response, self.tenant_user_role_url)

    def test_list_services(self):
        HTTPretty.register_uri(
            HTTPretty.GET,
            self.services_url,
            body=self._build_list_services_expected_response())

        actual_response = self.tenant_api_client.list_services()
        self._build_assertions(actual_response, self.services_url)

    def test_create_service(self):
        HTTPretty.register_uri(HTTPretty.POST, self.services_url)

        actual_response = self.tenant_api_client.create_service(
            name="Test-Service",
            description="Test Keystone Identity Service")
        self._build_assertions(actual_response, self.services_url)

    def test_delete_service(self):
        HTTPretty.register_uri(HTTPretty.DELETE, self.service_url)

        actual_response = self.tenant_api_client.delete_service(
            service_id=self.service_id)
        self._build_assertions(actual_response, self.service_url)

    def test_get_service(self):
        HTTPretty.register_uri(
            HTTPretty.GET,
            self.service_url,
            body=self._build_get_service_expected_response())

        actual_response = self.tenant_api_client.get_service(
            service_id=self.service_id)
        self._build_assertions(actual_response, self.service_url)

    def test_update_service(self):
        HTTPretty.register_uri(HTTPretty.PUT, self.service_url)

        actual_response = self.tenant_api_client.update_service(
            service_id=self.service_id)
        self._build_assertions(actual_response, self.service_url)

    def _build_assertions(self, actual_response, url):
        assert HTTPretty.last_request.headers['Content-Type'] == (
            'application/{0}'.format(self.serialize_format))
        assert HTTPretty.last_request.headers['Accept'] == (
            'application/{0}'.format(self.serialize_format))
        assert HTTPretty.last_request.headers['X-Auth-Token'] == (
            self.auth_token)
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

    def _build_list_users_expected_response(self):
        return {"users": [{"name": "user_name",
                           "id": "user_id",
                           "tenantId": "user_tenant_id",
                           "enabled": True,
                           "email": "user_email"}]}

    def _build_get_user_expected_response(self):
        return {"user": {"name": "user_name",
                         "id": "user_id",
                         "tenantId": "user_tenant_id",
                         "enabled": True,
                         "email": "user_email"}}

    def _build_list_services_expected_response(self):
        return {"OS-KSADM:services": [
            {"id": "19db0e41ddc64b8592c845e8950f5652",
             "type": "volume",
             "name": "cinder",
             "description": "Cinder Volume Service"}]}

    def _build_get_service_expected_response(self):
        return {"OS-KSADM:service": {
            "id": "665f687a9dbd41018149e48b31f4ea09",
            "type": "compute",
            "name": "nova",
            "description": "Nova Compute Service"}}
