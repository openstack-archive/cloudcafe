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

from cloudcafe.identity.v2_0.common.client import BaseIdentityAPIClient
from cloudcafe.identity.v2_0.extensions.osksadm.models import requests
from cloudcafe.identity.v2_0.models import responses
from cloudcafe.identity.v2_0.extensions.osksadm.models.responses import (
    Service, ServiceList)


class OSKSADM_Client(BaseIdentityAPIClient):
    def get_users(self, requestslib_kwargs=None):
        url = "{0}/users".format(self.url)
        return self.get(
            url, response_entity_type=responses.UserList,
            requestslib_kwargs=requestslib_kwargs)

    def create_user(
            self, enabled=None, email=None, name=None, password=None,
            tenant_id=None, requestslib_kwargs=None):
        url = "{0}/users".format(self.url)
        model = requests.CreateUser(
            enabled=enabled, email=email, name=name, password=password,
            tenant_id=tenant_id)
        return self.post(
            url, response_entity_type=responses.UserAlt, request_entity=model,
            requestslib_kwargs=requestslib_kwargs)

    def update_user(
            self, url_user_id, enabled=None, email=None, name=None,
            user_id=None,  tenant_id=None, requestslib_kwargs=None):
        url = "{0}/users/{1}".format(self.url, url_user_id)
        model = requests.UpdateUser(
            enabled=enabled, email=email, name=name, id_=user_id,
            tenant_id=tenant_id)
        return self.put(
            url, response_entity_type=responses.UserAlt, request_entity=model,
            requestslib_kwargs=requestslib_kwargs)

    def delete_user(self, user_id, requestslib_kwargs=None):
        url = "{0}/users/{1}".format(self.url, user_id)
        return self.delete(url, requestslib_kwargs=requestslib_kwargs)

    def get_user_global_roles(self, user_id, requestslib_kwargs=None):
        url = "{0}/users/{1}/roles".format(self.url, user_id)
        return self.get(
            url, response_entity_type=responses.RoleList,
            requestslib_kwargs=requestslib_kwargs)

    def add_global_role_to_user(
            self, user_id, role_id, requestslib_kwargs=None):
        url = "{0}/users/{1}/roles/{2}".format(self.url, user_id, role_id)
        return self.put(url, requestslib_kwargs=requestslib_kwargs)

    def delete_global_role_from_user(
            self, user_id, role_id, requestslib_kwargs=None):
        url = "{0}/users/{1}/roles/{2}".format(self.url, user_id, role_id)
        return self.delete(url, requestslib_kwargs=requestslib_kwargs)

    def create_tenant(
            self, name=None, description=None, enabled=None,
            requestslib_kwargs=None):
        url = "{0}/tenants".format(self.url)
        model = requests.CreateTenant(
            name=name, description=description, enabled=enabled)
        return self.post(
            url, response_entity_type=responses.Tenant, request_entity=model,
            requestslib_kwargs=requestslib_kwargs)

    def update_tenant(
            self, url_tenant_id, name=None, description=None, enabled=None,
            tenant_id=None, requestslib_kwargs=None):
        url = "{0}/tenants/{1}".format(self.url, url_tenant_id)
        model = requests.UpdateTenant(
            name=name, description=description, enabled=enabled, id_=tenant_id)
        return self.put(
            url, response_entity_type=responses.Tenant, request_entity=model,
            requestslib_kwargs=requestslib_kwargs)

    def delete_tenant(self, tenant_id, requestslib_kwargs=None):
        url = "{0}/tenants/{1}".format(self.url, tenant_id)
        return self.delete(url, requestslib_kwargs=requestslib_kwargs)

    def get_users_for_tenant(
            self, tenant_id, marker=None, limit=None, requestslib_kwargs=None):
        params = {}
        if marker:
            params["marker"] = marker
        if limit:
            params["limit"] = limit

        url = "{0}/tenants/{1}/users".format(self.url, tenant_id)
        return self.get(
            url, response_entity_type=responses.UserList, params=params,
            requestslib_kwargs=requestslib_kwargs)

    def add_role_to_user_for_tenant(
            self, tenant_id, user_id, role_id, requestslib_kwargs=None):
        url = "{0}/tenants/{1}/users/{2}/roles/OS-KSADM/{3}".format(
            self.url, tenant_id, user_id, role_id)
        return self.put(url, requestslib_kwargs=requestslib_kwargs)

    def delete_role_from_user_for_tenant(
            self, tenant_id, user_id, role_id, requestslib_kwargs=None):
        url = "{0}/tenants/{1}/users/{2}/roles/OS-KSADM/{3}".format(
            self.url, tenant_id, user_id, role_id)
        return self.delete(url, requestslib_kwargs=requestslib_kwargs)

    def get_role_by_name(self, name, requestslib_kwargs=None):
        url = "{0}/OS-KSADM/roles".format(self.url)
        params = {"name": name}

        return self.get(
            url, params=params, response_entity_type=responses.Role,
            requestslib_kwargs=requestslib_kwargs)

    def create_role(
            self, role_id=None, name=None, description=None,
            requestslib_kwargs=None):
        url = "{0}/OS-KSADM/roles".format(self.url)
        model = requests.CreateRole(
            id_=role_id, name=name, description=description)
        return self.post(
            url, response_entity_type=responses.Role, request_entity=model,
            requestslib_kwargs=requestslib_kwargs)

    def get_roles(self, requestslib_kwargs=None):
        url = "{0}/OS-KSADM/roles".format(self.url)
        return self.get(
            url, response_entity_type=responses.RoleList,
            requestslib_kwargs=requestslib_kwargs)

    def get_role_by_id(self, role_id, requestslib_kwargs=None):
        url = "{0}/OS-KSADM/roles/{1}".format(self.url, role_id)
        return self.get(
            url, response_entity_type=responses.Role,
            requestslib_kwargs=requestslib_kwargs)

    def delete_role(
            self, role_id, requestslib_kwargs=None):
        url = "{0}/OS-KSADM/roles/{1}".format(self.url, role_id)
        return self.delete(url, requestslib_kwargs=requestslib_kwargs)

    def get_services(self, marker=None, limit=None, requestslib_kwargs=None):
        params = {}
        if marker:
            params["marker"] = marker
        if limit:
            params["limit"] = limit
        url = "{0}/OS-KSADM/services".format(self.url)
        return self.get(
            url, response_entity_type=ServiceList,
            requestslib_kwargs=requestslib_kwargs)

    def create_service(
            self, service_id=None, name=None, type_=None, description=None,
            requestslib_kwargs=None):
        url = "{0}/OS-KSADM/services".format(self.url)
        model = requests.CreateService(
            id_=service_id, name=name, type_=type_, description=description)
        return self.post(
            url, request_entity=model, response_entity_type=Service,
            requestslib_kwargs=requestslib_kwargs)

    def get_service_by_name(self, name=None, requestslib_kwargs=None):
        url = "{0}/OS-KSADM/services".format(self.url)
        params = {"name": name}
        return self.get(
            url, params=params, response_entity_type=Service,
            requestslib_kwargs=requestslib_kwargs)

    def get_service_by_id(self, service_id, requestslib_kwargs=None):
        url = "{0}/OS-KSADM/services/{1}".format(self.url, service_id)
        return self.get(
            url, response_entity_type=Service,
            requestslib_kwargs=requestslib_kwargs)

    def delete_service(self, service_id, requestslib_kwargs=None):
        url = "{0}/OS-KSADM/services/{1}".format(self.url, service_id)
        return self.delete(url, requestslib_kwargs=requestslib_kwargs)
