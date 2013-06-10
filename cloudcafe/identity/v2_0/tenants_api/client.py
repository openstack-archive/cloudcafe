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

from cafe.engine.clients.rest import AutoMarshallingRestClient
from cloudcafe.identity.v2_0.tenants_api.models.responses.tenant import \
    Tenants, Tenant
from cloudcafe.identity.v2_0.tenants_api.models.responses.role import \
    Roles
from cloudcafe.identity.v2_0.tenants_api.models.responses.user import User
from cloudcafe.identity.v2_0.tokens_api.models.requests.role import Role
from cloudcafe.identity.v2_0.users_api.models.responses.user import \
    Users

_version = 'v2.0'


class TenantsAPI_Client(AutoMarshallingRestClient):
    def __init__(self, url, auth_token,
                 serialize_format=None, deserialize_format=None):
        """
        @param url: Base URL for the keystone service
        @type url: String
        @param auth_token: Auth token to be used for all requests
        @type auth_token: String
        @param serialize_format: Format for serializing requests
        @type serialize_format: String
        @param deserialize_format: Format for de-serializing responses
        @type deserialize_format: String
        """

        super(TenantsAPI_Client, self).__init__(
            serialize_format, deserialize_format)
        self.base_url = '{0}/{1}'.format(url, _version)
        self.default_headers['Content-Type'] = 'application/{0}'.format(
            serialize_format)
        self.default_headers['Accept'] = 'application/{0}'.format(
            serialize_format)
        self.default_headers['X-Auth-Token'] = auth_token

    def list_tenants(self, requestslib_kwargs=None):
        """
        @summary: Lists all tenants. Maps to /tenants
        @return: server_response
        @rtype: Response
        """

        url = '%s/tenants' % self.base_url
        server_response = self.request('GET', url,
                                       response_entity_type=Tenants,
                                       requestslib_kwargs=requestslib_kwargs)
        return server_response

    def get_tenant(self, tenant_id, requestslib_kwargs=None):
        """
        @summary: Returns a tenant based off passed tenant_id.
         Maps to /tenants/{tenantid}
        @param tenant_id: The ID for the tenant
        @type tenant_id: String
        @return: server_response
        @rtype: Response
        """

        url = '%s/tenants/%s' % (self.base_url, tenant_id)
        server_response = self.request('GET', url,
                                       response_entity_type=Tenant,
                                       requestslib_kwargs=requestslib_kwargs)
        return server_response

    def create_tenant(self, name=None, description=None,
                      enabled=None, requestslib_kwargs=None):
        """
        @summary: Creates a tenant given the provided parameters
         Maps to /tenants
        @param name: The name for the tenant
        @type name: String
        @param description: The description of the tenant
        @type description: String
        @param enabled: The status of the tenant
        @type name: Boolean
        @return: server_response
        @rtype: Response
        """

        url = '%s/tenants' % self.base_url
        tenant_request_object = Tenant(name=name, description=description,
                                       enabled=enabled)
        server_response = self.request('POST', url,
                                       response_entity_type=Tenant,
                                       request_entity=tenant_request_object,
                                       requestslib_kwargs=requestslib_kwargs)
        return server_response

    def update_tenant(self, tenant_id, name=None, description=None,
                      enabled=None, requestslib_kwargs=None):
        """
        @summary: Creates a tenant given the provided parameters
         Maps to /tenants
        @param tenant_id: The id of an existing tenant.
        @type tenant_id: String
        @param name: The name for the tenant
        @type name: String
        @param description: The description of the tenant
        @type description: String
        @param enabled: The status of the tenant
        @type name: Boolean
        @return: server_response
        @rtype: Response
        """
        url = '%s/tenants/%s' % (self.base_url, tenant_id)
        tenant_request_object = Tenant(id_=tenant_id, name=name,
                                       description=description,
                                       enabled=enabled)
        server_response = self.request('PUT', url,
                                       response_entity_type=Tenant,
                                       request_entity=tenant_request_object,
                                       requestslib_kwargs=requestslib_kwargs)
        return server_response

    def delete_tenant(self, tenant_id, requestslib_kwargs=None):
        """
        @summary: Deletes the specified tenant
        @param tenant_id: The id of a tenant
        @type tenant_id: String
        @return: resp
        @rtype: Requests.response
        """

        url = '%s/tenants/%s' % (self.base_url, tenant_id)
        response = self.request('DELETE', url,
                                requestslib_kwargs=requestslib_kwargs)
        return response

    def create_user_for_a_tenant(self, id_=None, tenant_id=None, name=None,
                                 enabled=None, email=None,
                                 requestslib_kwargs=None):
        """
        @summary: Creates a user for a given tenant
        """

        url = '%s/tenants/%s/users' % (self.base_url, tenant_id)
        user_request_object = User(id_=id_, tenant_id=tenant_id, name=name,
                                   enabled=enabled, email=email)
        server_response = self.request('POST', url,
                                       response_entity_type=User,
                                       request_entity=user_request_object,
                                       requestslib_kwargs=requestslib_kwargs)
        return server_response

    def get_users_for_tenant(self, tenant_id, requestslib_kwargs=None):
        """
        @summary: Returns all the users that a tenant has.
         Maps to /tenants/{tenant_id}/users.
        @param tenant_id: The ID for the tenant
        @type tenant_id: String
        @return: server_response
        @rtype: Response
        """

        url = '%s/tenants/%s/users' % (self.base_url, tenant_id)
        server_response = self.request('GET', url,
                                       response_entity_type=Users,
                                       requestslib_kwargs=requestslib_kwargs)
        return server_response

    def create_role_for_tenant_user(self, id_=None, name=None,
                                    tenant_id=None, user_id=None,
                                    requestslib_kwargs=None):
        """
        @summary: Creates a role for a given tenant user
        """

        url = '%s/tenants/%s/users/%s/roles' % (
            self.base_url, tenant_id, user_id)

        role_request_object = Role(id=id_, name=name)
        server_response = self.request('POST', url,
                                       response_entity_type=Role,
                                       request_entity=role_request_object,
                                       requestslib_kwargs=requestslib_kwargs)
        return server_response

    def get_users_roles_on_tenant(self, tenant_id, user_id,
                                  requestslib_kwargs=None):
        """
        @summary: Returns a specific users roles for a given tenant
        @param tenant_id: The id of the tenant
        @type tenant_id: String
        @param user_id: The id of the user
        @type user_id: String
        @return: server_response
        @rtype: Response
        """

        url = '%s/tenants/%s/users/%s/roles' % (
            self.base_url, tenant_id, user_id)
        server_response = self.request('GET', url,
                                       response_entity_type=Roles,
                                       requestslib_kwargs=requestslib_kwargs)
        return server_response
