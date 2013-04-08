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
import json

from cloudcafe.extensions.rax_auth.v2_0.tokens_api.models.base import \
    BaseIdentityModel, BaseIdentityListModel


class Access(BaseIdentityModel):

    TAG = 'access'

    def __init__(self):
        self.metadata = {}
        self.service_catalog = ServiceCatalog()
        self.user = User()
        self.token = Token()

    def get_service(self, name):
        for service in self.service_catalog:
            if service.name == name:
                return service
        return None

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._dict_to_obj(json_dict.get(cls.TAG))

    @classmethod
    def _dict_to_obj(cls, json_dict):

        access = Access()
        access.metadata = json_dict.get('metadata')
        access.service_catalog = ServiceCatalog._list_to_obj(
            json_dict.get(ServiceCatalog.TAG))
        access.user = User._dict_to_obj(json_dict.get(User.TAG))
        access.token = Token._dict_to_obj(json_dict.get(Token.TAG))
        return access


class ServiceCatalog(BaseIdentityListModel):
    TAG = 'serviceCatalog'

    @classmethod
    def _list_to_obj(cls, service_dict_list):
        service_catalog = ServiceCatalog()
        for service_dict in service_dict_list:
            service = Service._dict_to_obj(service_dict)
            service_catalog.append(service)

        return service_catalog


class Service(BaseIdentityModel):

    def __init__(self):
        self.endpoints = EndpointList()
        self.endpoint_links = []
        self.name = None
        self.type = None

    def get_endpoint(self, region):
        """
        Returns the endpoint that matches the provided region,
        or None if such an endpoint is not found
        """
        for ep in self.endpoints:
            if getattr(ep, 'region'):
                if str(ep.region).lower() == str(region).lower():
                    return ep

    @classmethod
    def _dict_to_obj(cls, json_dict):
        service = Service()
        service.endpoints = EndpointList._list_to_obj(
            json_dict.get(EndpointList.TAG))
        service.endpoint_links = json_dict.get('endpoints_links')
        service.name = json_dict.get('name')
        service.type = json_dict.get('type')

        return service


class EndpointList(BaseIdentityListModel):
    TAG = 'endpoints'

    @classmethod
    def _list_to_obj(cls, endpoint_dict_list):
        endpoint_list = EndpointList()
        for endpoint_dict in endpoint_dict_list:
            endpoint = Endpoint._dict_to_obj(endpoint_dict)
            endpoint_list.append(endpoint)

        return endpoint_list


class Endpoint(BaseIdentityModel):

    def __init__(self, admin_url, internal_url, public_url,
                 region, id):
        self.admin_url = admin_url
        self.internal_url = internal_url
        self.public_url = public_url
        self.region = region
        self.id_ = id

    @classmethod
    def _dict_to_obj(cls, json_dict):
        endpoint = Endpoint(json_dict.get('adminURL'),
                            json_dict.get('internalURL'),
                            json_dict.get('publicURL'),
                            json_dict.get('region'),
                            json_dict.get('id'))
        return endpoint


class Token(BaseIdentityModel):
    TAG = 'token'

    def __init__(self):
        self.expires = None
        self.issued_at = None
        self.id_ = None
        self.tenant = Tenant()

    @classmethod
    def _dict_to_obj(cls, json_dict):
        token_model = Token()
        token_model.tenant = Tenant._dict_to_obj(json_dict.get('tenant'))
        token_model.expires = json_dict.get('expires')
        token_model.issued_at = json_dict.get('issued_at')
        token_model.id_ = json_dict.get('id')

        return token_model


class Tenant(BaseIdentityModel):
    TAG = 'tenant'

    def __init__(self):
        self.description = None
        self.enabled = None
        self.id_ = None
        self.name = None

    @classmethod
    def _dict_to_obj(cls, json_dict):
        tenant = Tenant()
        tenant.description = json_dict.get('description')
        tenant.enabled = json_dict.get('enabled')
        tenant.id_ = json_dict.get('id')
        tenant.name = json_dict.get('name')

        return tenant


class User(BaseIdentityModel):
    TAG = 'user'

    def __init__(self):
        self.id_ = None
        self.name = None
        self.roles = RoleList()
        self.role_links = []
        self.username = None

    @classmethod
    def _dict_to_obj(cls, json_dict):
        user = User()
        user.id_ = json_dict.get('id')
        user.name = json_dict.get('name')
        user.roles = RoleList._list_to_obj(json_dict.get(RoleList.TAG))
        user.role_links = json_dict.get('role_links')
        user.username = json_dict.get('username')

        return user


class RoleList(BaseIdentityListModel):
    TAG = 'roles'

    @classmethod
    def _list_to_obj(cls, role_dict_list):
        role_list = RoleList()
        for role_dict in role_dict_list:
            role = Role(name=role_dict.get('name'))
            role_list.append(role)

        return role_list


class Role(BaseIdentityListModel):

    def __init__(self, name=None):
        self.name = name
