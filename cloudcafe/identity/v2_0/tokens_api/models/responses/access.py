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
from cloudcafe.identity.v2_0.tokens_api.models.base import \
    BaseIdentityModel, BaseIdentityListModel


class Access(BaseIdentityModel):
    def __init__(self, metadata=None, service_catalog=None,
                 user=None, token=None):
        super(Access, self).__init__()
        self.metadata = metadata
        self.service_catalog = service_catalog
        self.user = user
        self.token = token

    def get_service(self, name):
        for service in self.service_catalog:
            if service.name == name:
                return service

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._dict_to_obj(json_dict.get('access'))

    @classmethod
    def _dict_to_obj(cls, json_dict):
        access = Access(
            metadata=json_dict.get('metadata'),
            service_catalog=ServiceCatalog._list_to_obj(
                json_dict.get('serviceCatalog')),
            user=User._dict_to_obj(json_dict.get('user')),
            token=Token._dict_to_obj(json_dict.get('token')))
        return access


class ServiceCatalog(BaseIdentityListModel):
    def __init__(self, services=None):
        super(ServiceCatalog, self).__init__()
        self.extend(services or [])

    @classmethod
    def _list_to_obj(cls, service_dict_list):
        service_catalog = ServiceCatalog()
        for service_dict in service_dict_list:
            service = Service._dict_to_obj(service_dict)
            service_catalog.append(service)
        return service_catalog


class Service(BaseIdentityModel):
    def __init__(self, endpoints=None, endpoint_links=None,
                 name=None, type_=None):
        """
        @param endpoints:
        @type: EndpointList
        """
        super(Service, self).__init__()
        self.endpoints = endpoints
        self.endpoint_links = endpoint_links
        self.name = name
        self.type_ = type_

    def get_endpoint(self, region):
        """
        Returns the endpoint that matches the provided region,
        or None if such an endpoint is not found
        """
        for endpoint in self.endpoints:
            if getattr(endpoint, 'region'):
                if str(endpoint.region).lower() == str(region).lower():
                    return endpoint

    @classmethod
    def _dict_to_obj(cls, json_dict):
        service = Service(
            endpoints=EndpointList._list_to_obj(json_dict.get('endpoints')),
            endpoint_links=json_dict.get('endpoints_links'),
            name=json_dict.get('name'),
            type_=json_dict.get('type'))
        return service


class EndpointList(BaseIdentityListModel):
    def __init__(self, endpoints=None):
        super(EndpointList, self).__init__()
        self.extend(endpoints or [])

    @classmethod
    def _list_to_obj(cls, endpoint_dict_list):
        endpoint_list = EndpointList()
        for endpoint_dict in endpoint_dict_list:
            endpoint = Endpoint._dict_to_obj(endpoint_dict)
            endpoint_list.append(endpoint)
        return endpoint_list


class Endpoint(BaseIdentityModel):
    def __init__(self, id_=None, admin_url=None,
                 internal_url=None, public_url=None, region=None):
        super(Endpoint, self).__init__()
        self.admin_url = admin_url
        self.internal_url = internal_url
        self.public_url = public_url
        self.region = region
        self.id_ = id_

    @classmethod
    def _dict_to_obj(cls, json_dict):
        endpoint = Endpoint(admin_url=json_dict.get('adminURL'),
                            internal_url=json_dict.get('internalURL'),
                            public_url=json_dict.get('publicURL'),
                            region=json_dict.get('region'),
                            id_=json_dict.get('id'))
        return endpoint


class Token(BaseIdentityModel):
    def __init__(self, id_=None, issued_at=None,
                 expires=None, tenant=None):
        super(Token, self).__init__()
        self.expires = expires
        self.issued_at = issued_at
        self.id_ = id_
        self.tenant = tenant

    @classmethod
    def _dict_to_obj(cls, json_dict):
        token = Token(tenant=Tenant._dict_to_obj(json_dict.get('tenant')),
                      expires=json_dict.get('expires'),
                      issued_at=json_dict.get('issued_at'),
                      id_=json_dict.get('id'))
        return token


class Tenant(BaseIdentityModel):
    def __init__(self, id_=None, name=None,
                 enabled=None, description=None):
        super(Tenant, self).__init__()
        self.id_ = id_
        self.name = name
        self.enabled = enabled
        self.description = description

    @classmethod
    def _dict_to_obj(cls, json_dict):
        tenant = Tenant(id_=json_dict.get('id'),
                        name=json_dict.get('name'),
                        enabled=json_dict.get('enabled'),
                        description=json_dict.get('description'))
        return tenant


class User(BaseIdentityModel):
    def __init__(self, id_=None, name=None,
                 username=None, roles=None, roles_links=None):
        """
        @param id_
        @return:
        @param roles
        @type RoleList
        """
        super(User, self).__init__()
        self.id_ = id_
        self.name = name
        self.username = username
        self.roles = roles
        self.roles_links = roles_links

    @classmethod
    def _dict_to_obj(cls, json_dict):
        user = User(id_=json_dict.get('id'),
                    name=json_dict.get('name'),
                    roles=RoleList._list_to_obj(json_dict.get('roles')),
                    roles_links=json_dict.get('roles_links'),
                    username=json_dict.get('username'))
        return user


class RoleList(BaseIdentityListModel):
    def __init__(self, roles=None):
        super(RoleList, self).__init__()
        self.extend(roles or [])

    @classmethod
    def _list_to_obj(cls, role_dict_list):
        role_list = RoleList()
        for role_dict in role_dict_list:
            role = Role(name=role_dict.get('name'))
            role_list.append(role)
        return role_list


class Role(BaseIdentityListModel):

    def __init__(self, id_=None, name=None):
        super(Role, self).__init__()
        self.id_ = id_
        self.name = name
