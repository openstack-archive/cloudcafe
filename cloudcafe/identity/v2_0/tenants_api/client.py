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

from cafe.engine.http.client import AutoMarshallingHTTPClient
from cloudcafe.identity.v2_0.tenants_api.models.responses.tenant import \
    Tenants, Tenant
from cloudcafe.identity.v2_0.tenants_api.models.responses.role import \
    Roles, Role
from cloudcafe.identity.v2_0.tenants_api.models.responses.user import \
    Users, User
from cloudcafe.identity.v2_0.common.models.constants import AdminExtensions
from cloudcafe.identity.v2_0.tenants_api.models.responses.service import \
    Service, Services

_version = 'v2.0'
_admin_extensions = AdminExtensions.OS_KS_ADM


class TenantsAPI_Client(AutoMarshallingHTTPClient):
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

        url = '{0}/tenants'.format(self.base_url)
        response = self.request('GET', url,
                                response_entity_type=Tenants,
                                requestslib_kwargs=requestslib_kwargs)
        return response

    def get_tenant(self, tenant_id, requestslib_kwargs=None):
        """
        @summary: Returns a tenant based on a passed tenant_id.
         Maps to /tenants/{tenant_id}
        @param tenant_id: The ID for the tenant
        @type tenant_id: String
        @return: response
        @rtype: Response
        """

        url = '{0}/tenants/{1}'.format(self.base_url, tenant_id)
        response = self.request('GET', url,
                                response_entity_type=Tenant,
                                requestslib_kwargs=requestslib_kwargs)
        return response

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

        url = '{0}/tenants'.format(self.base_url)
        tenant_request_object = Tenant(name=name, description=description,
                                       enabled=enabled)
        response = self.request('POST', url,
                                response_entity_type=Tenant,
                                request_entity=tenant_request_object,
                                requestslib_kwargs=requestslib_kwargs)
        return response

    def update_tenant(self, tenant_id, name=None, description=None,
                      enabled=None, requestslib_kwargs=None):
        """
        @summary: Updates a tenant given the provided parameters
         Maps to /tenants
        @param tenant_id: The ID of an existing tenant.
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
        url = '{0}/tenants/{1}'.format(self.base_url, tenant_id)
        tenant_request_object = Tenant(id_=tenant_id, name=name,
                                       description=description,
                                       enabled=enabled)
        response = self.request('PUT', url,
                                response_entity_type=Tenant,
                                request_entity=tenant_request_object,
                                requestslib_kwargs=requestslib_kwargs)
        return response

    def delete_tenant(self, tenant_id, requestslib_kwargs=None):
        """
        @summary: Deletes the specified tenant
        @param tenant_id: The ID of a tenant
        @type tenant_id: String
        @return: resp
        @rtype: Requests.response
        """

        url = '{0}/tenants/{1}'.format(self.base_url, tenant_id)
        response = self.request('DELETE', url,
                                requestslib_kwargs=requestslib_kwargs)
        return response

    def list_users(self, requestslib_kwargs=None):
        """
        @summary: Lists all users. Maps to /users
        @return: server_response
        @rtype: Response
        """

        url = '{0}/users'.format(self.base_url)
        response = self.request('GET', url,
                                response_entity_type=Users,
                                requestslib_kwargs=requestslib_kwargs)
        return response

    def get_user(self, user_id, requestslib_kwargs=None):
        """
        @summary: Returns a user based on a passed user_id.
         Maps to /users/{user_id}
        @param user_id: The ID for the user
        @type user_id: String
        @return: server_response
        @rtype: Response
        """

        url = '{0}/users/{1}'.format(self.base_url, user_id)
        response = self.request('GET', url,
                                response_entity_type=User,
                                requestslib_kwargs=requestslib_kwargs)
        return response

    def create_user_for_a_tenant(self, id_=None, tenant_id=None, name=None,
                                 enabled=None, email=None,
                                 requestslib_kwargs=None):
        """
        @summary: Creates a user for a given tenant
        """

        url = '{0}/users'.format(self.base_url)
        user_request_object = User(id_=id_, tenant_id=tenant_id, name=name,
                                   enabled=enabled, email=email)
        response = self.request('POST', url,
                                response_entity_type=User,
                                request_entity=user_request_object,
                                requestslib_kwargs=requestslib_kwargs)
        return response

    def update_user(self, user_id=None, name=None, enabled=None,
                    email=None, requestslib_kwargs=None):
        """
        @summary: Updates a user given the provided parameters
         Maps to /users/{user_id}
        @param user_id: The ID of an existing tenant.
        @type user_id: String
        @param name: The name for the user
        @type name: String
        @param user_id: The id of the user
        @type user_id: String
        @param enabled: The status of the user
        @type name: Boolean
        @return: server_response
        @rtype: Response
        """

        url = '{0}/users/{1}'.format(self.base_url, user_id)
        user_request_object = User(id_=user_id, name=name,
                                   tenant_id=user_id,
                                   enabled=enabled, email=email)
        response = self.request('PUT', url,
                                response_entity_type=User,
                                request_entity=user_request_object,
                                requestslib_kwargs=requestslib_kwargs)
        return response

    def delete_user(self, user_id, requestslib_kwargs=None):
        """
        @summary: Deletes the specified user
        @param user_id: The ID of a user
        @type user_id: String
        @return: resp
        @rtype: Requests.response
        """

        url = '{0}/users/{1}'.format(self.base_url, user_id)
        response = self.request('DELETE', url,
                                requestslib_kwargs=requestslib_kwargs)
        return response

    def get_users_for_tenant(self, tenant_id, requestslib_kwargs=None):
        """
        @summary: Returns all the users that a given tenant has.
        Maps to /tenants/{tenant_id}/users.
        @summary: Returns all the users that a tenant has.
        Maps to /tenants/{tenant_id}/users.
        @summary: Returns all the users that a tenant has.
        Maps to /tenants/{tenant_id}/users.
        Maps to /tenants/{tenant_id}/users.
        @summary: Returns all the users that a tenant has.
        Maps to /tenants/{tenant_id}/users.
        @param tenant_id: The ID for the tenant
        @type tenant_id: String
        @return: server_response
        @rtype: Response
        """

        url = '{0}/tenants/{1}/users'.format(self.base_url, tenant_id)
        response = self.request('GET', url,
                                response_entity_type=Users,
                                requestslib_kwargs=requestslib_kwargs)
        return response

    def assign_role_to_tenant_user(self, role_id=None, name=None,
                                   tenant_id=None, user_id=None,
                                   requestslib_kwargs=None):
        """
        @summary: Assigns a role to a given tenant user
        """

        url = '{0}/tenants/{1}/users/{2}/roles/{3}/{4}'.format(
            self.base_url,
            tenant_id,
            user_id,
            _admin_extensions,
            role_id)

        response = self.request('PUT', url,
                                response_entity_type=Role,
                                requestslib_kwargs=requestslib_kwargs)
        return response

    def get_users_roles_on_tenant(self, tenant_id, user_id,
                                  requestslib_kwargs=None):
        """
        @summary: Returns a specific roles for a given tenant user
        @param tenant_id: The ID of the tenant
        @type tenant_id: String
        @param user_id: The ID of the user
        @type user_id: String
        @return: response
        @rtype: Response
        """

        url = '{0}/tenants/{1}/users/{2}/roles'.format(self.base_url,
                                                       tenant_id, user_id)
        response = self.request('GET', url,
                                response_entity_type=Roles,
                                requestslib_kwargs=requestslib_kwargs)
        return response

    def remove_role_of_tenant_user(self, tenant_id=None,
                                   user_id=None, role_id=None,
                                   requestslib_kwargs=None):
        """
        @summary: Deletes the specified roles for a tenant user
        @param tenant_id: The id of a tenant
        @type tenant_id: String
        @param user_id: The ID of a user
        @type user_id: String
        @param role_id: The ID of a role
        @type role_id: String
        @return: resp
        @rtype: Requests.response
        """

        url = '{0}/tenants/{1}/users/{2}/roles/{3}/{4}'.format(
            self.base_url,
            tenant_id,
            user_id,
            _admin_extensions,
            role_id)

        response = self.request('DELETE', url,
                                requestslib_kwargs=requestslib_kwargs)
        return response

    def create_service(self, name=None, type_=None,
                       description=None, requestslib_kwargs=None):
        """
        @summary: Creates a service given the provided parameters
         Maps to /services
        @param name: The name for the service
        @type name: String
        @param type_: The type of the service
        @type type_: String
        @param description: The description of the service
        @type description: String
        @return: response
        @rtype: Response
        """

        url = '{0}/{1}/services'.format(self.base_url,
                                        _admin_extensions)
        service_request_object = Service(name=name,
                                         type_=type_,
                                         description=description)

        response = self.request('POST', url,
                                response_entity_type=Service,
                                request_entity=service_request_object,
                                requestslib_kwargs=requestslib_kwargs)

        return response

    def delete_service(self, service_id, requestslib_kwargs=None):
        """
        @summary: Deletes the specified service
        @param service_id: The ID of a service
        @type service_id: String
        @return: resp
        @rtype: Requests.response
        """

        url = '{0}/{1}/services/{2}'.format(self.base_url,
                                            _admin_extensions,
                                            service_id)
        response = self.request('DELETE', url,
                                requestslib_kwargs=requestslib_kwargs)

        return response

    def list_services(self, requestslib_kwargs=None):
        """
        @summary: Lists all services. Maps to /services
        @return: response
        @rtype: Response
        """

        url = '{0}/{1}/services'.format(self.base_url, _admin_extensions)
        response = self.request('GET', url,
                                response_entity_type=Services,
                                requestslib_kwargs=requestslib_kwargs)

        return response

    def get_service(self, service_id, requestslib_kwargs=None):
        """
        @summary: Returns a service based of passed service_id.
         Maps to /services/{service_id}
        @param service_id: The ID for the service
        @type service_id: String
        @return: response
        @rtype: Response
        """

        url = '{0}/{1}/services/{2}'.format(self.base_url,
                                            _admin_extensions,
                                            service_id)
        response = self.request('GET', url,
                                response_entity_type=Service,
                                requestslib_kwargs=requestslib_kwargs)

        return response

    def update_service(self, service_id, name=None, type_=None,
                       description=None, requestslib_kwargs=None):
        """
        @summary: Updates a service given the provided parameters
         Maps to /services
        @param service_id: The ID of an existing service.
        @type service_id: String
        @param name: The name for the service
        @type name: String
        @param description: The description of the service
        @type description: String
        @param type_: The type of the service
        @type type_: String
        @return: response
        @rtype: Response
        """

        url = '{0}/{1}/services/{2}'.format(self.base_url,
                                            _admin_extensions,
                                            service_id)
        service_request_object = Service(id_=service_id,
                                         name=name,
                                         type_=type_,
                                         description=description)

        response = self.request('PUT', url,
                                response_entity_type=Service,
                                request_entity=service_request_object,
                                requestslib_kwargs=requestslib_kwargs)

        return response
