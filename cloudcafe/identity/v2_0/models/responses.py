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

from cloudcafe.identity.common.models.base import (
    BaseIdentityModel, BaseIdentityListModel)


class UserList(BaseIdentityListModel):
    @classmethod
    def _xml_ele_to_obj(cls, element):
        users = cls()
        if element.tag.lower() != "users":
            raise Exception("wrong element")
        for user in element.getchildren():
            users.append(UserAlt._xml_ele_to_obj(user))
        return users

    @classmethod
    def _dict_to_obj(cls, data_dict):
        users = cls()
        for user in data_dict.get('users'):
            users.append(UserAlt._dict_to_obj(user))
        return users


class UserAlt(BaseIdentityModel):
    def __init__(self, enabled=None, email=None, name=None, id_=None):
        super(UserAlt, self).__init__()
        self.enabled = enabled
        self.email = email
        self.name = name
        self.id_ = id_

    @classmethod
    def _xml_ele_to_obj(cls, element):
        if element.tag.lower() != "user":
            raise Exception("wrong element")
        enabled = True if element.attrib.get('enabled') == "true" else False
        return cls(enabled=enabled,
                   email=element.attrib.get('email'),
                   name=element.attrib.get('name'),
                   id_=element.attrib.get('id'))

    @classmethod
    def _dict_to_obj(cls, data_dict):
        return cls(enabled=data_dict.get('enabled'),
                   email=data_dict.get('email'),
                   name=data_dict.get('name'),
                   id_=data_dict.get('id'))

    @classmethod
    def _json_to_obj(cls, serialized_str):
        data_dict = json.loads(serialized_str)
        return cls._dict_to_obj(data_dict.get('user'))


class RoleList(BaseIdentityListModel):
    # leaving roles_links out because it is not in the xml and is always an
    # empty list
    @classmethod
    def _xml_ele_to_obj(cls, element):
        roles = cls()
        if element.tag.lower() != "roles":
            raise Exception("wrong element")
        for role in element.getchildren():
            roles.append(Role._xml_ele_to_obj(role))
        return roles

    @classmethod
    def _dict_to_obj(cls, data_dict):
        roles = cls()
        for role in data_dict.get('roles'):
            roles.append(Role._dict_to_obj(role))
        return roles


class Role(BaseIdentityModel):
    def __init__(self, id_=None, name=None, description=None):
        super(Role, self).__init__()
        self.id_ = id_
        self.name = name
        self.description = description

    @classmethod
    def _xml_ele_to_obj(cls, element):
        if element.tag.lower() != "role":
            raise Exception("wrong element")
        return cls(id_=element.attrib.get('id'),
                   name=element.attrib.get('name'),
                   description=element.attrib.get('description'))

    @classmethod
    def _dict_to_obj(cls, data_dict):
        return cls(id_=data_dict.get('id'),
                   name=data_dict.get('name'),
                   description=data_dict.get('description'))

    @classmethod
    def _json_to_obj(cls, serialized_str):
        data_dict = json.loads(serialized_str)
        return cls._dict_to_obj(data_dict.get('role'))


class TenantList(BaseIdentityListModel):
    # leaving tenants_links out because it is not in the xml and is always an
    # empty list
    @classmethod
    def _xml_ele_to_obj(cls, element):
        tenants = cls()
        if element.tag.lower() != "tenants":
            raise Exception("wrong element")
        for tenant in element.getchildren():
            tenants.append(Tenant._xml_ele_to_obj(tenant))
        return tenants

    @classmethod
    def _dict_to_obj(cls, data_dict):
        tenants = cls()
        for tenant in data_dict.get('tenants'):
            tenants.append(Tenant._dict_to_obj(tenant))
        return tenants


class Tenant(BaseIdentityModel):
    def __init__(self, enabled=None, description=None, name=None, id_=None):
        super(Tenant, self).__init__()
        self.enabled = enabled
        self.description = description
        self.name = name
        self.id_ = id_

    @classmethod
    def _xml_ele_to_obj(cls, element):
        if element.tag.lower() != "tenant":
            raise Exception("wrong element")
        enabled = True if element.attrib.get('enabled') == "true" else False
        description = element.find('description')
        description = "" if description is None else description.text
        return cls(enabled=enabled,
                   description=description,
                   name=element.attrib.get('name'),
                   id_=element.attrib.get('id'))

    @classmethod
    def _dict_to_obj(cls, data_dict):
        return cls(description=data_dict.get('description'),
                   enabled=data_dict.get('enabled'),
                   id_=data_dict.get('id'),
                   name=data_dict.get('name'))

    @classmethod
    def _json_to_obj(cls, serialized_str):
        data_dict = json.loads(serialized_str)
        return cls._dict_to_obj(data_dict.get('tenant'))


class AuthResponse(BaseIdentityModel):
    def __init__(
            self, token=None, service_catalog=None, user=None, metadata=None):
        super(AuthResponse, self).__init__()
        self.token = token
        self.service_catalog = service_catalog
        self.user = user
        self.metadata = metadata

    def get_service(self, name):
        for service in self.service_catalog:
            if service.name == name:
                return service
        return None

    @classmethod
    def _dict_to_obj(cls, data):
        return cls(
            token=AuthResponseToken._dict_to_obj(data.get('token')),
            metadata=Metadata._dict_to_obj(data.get('metadata')),
            user=User._dict_to_obj(data.get('user')),
            service_catalog=ServiceCatalog._dict_to_obj(
                data.get('serviceCatalog')))

    @classmethod
    def _json_to_obj(cls, serialized_str):
        data_dict = json.loads(serialized_str)
        return cls._dict_to_obj(data_dict.get("access"))

    @classmethod
    def _xml_ele_to_obj(cls, ele):
        return cls(
            token=AuthResponseToken._xml_ele_to_obj(ele.find('token')),
            metadata=Metadata._xml_ele_to_obj(ele.find('metadata')),
            user=User._xml_ele_to_obj(ele.find('user')),
            service_catalog=ServiceCatalog._xml_ele_to_obj(
                ele.find('serviceCatalog')))


class AuthResponseToken(BaseIdentityModel):
    def __init__(self, id_=None, issued_at=None, expires=None, tenant=None):
        super(AuthResponseToken, self).__init__()
        self.id_ = id_
        self.issued_at = issued_at
        self.expires = expires
        self.tenant = tenant

    @classmethod
    def _dict_to_obj(cls, data):
        return cls(id_=data.get('id'),
                   expires=data.get('expires'),
                   issued_at=data.get('issued_at'),
                   tenant=Tenant._dict_to_obj(data.get('tenant')))

    @classmethod
    def _xml_ele_to_obj(cls, ele):
        return cls(id_=ele.attrib.get('id'),
                   expires=ele.attrib.get('expires'),
                   issued_at=ele.attrib.get('issued_at'),
                   tenant=Tenant._xml_ele_to_obj(ele.find('tenant')))


class ServiceCatalog(BaseIdentityListModel):

    @classmethod
    def _dict_to_obj(cls, obj_list):
        return ServiceCatalog([Service._dict_to_obj(obj) for obj in obj_list])

    @classmethod
    def _xml_ele_to_obj(cls, ele):
        return ServiceCatalog([Service._xml_ele_to_obj(element) for element in
                               ele.findall("service")])


class User(BaseIdentityModel):
    def __init__(
            self, id_=None, name=None, username=None, roles=None,
            roles_links=None):
        super(User, self).__init__()
        self.id_ = id_
        self.name = name
        self.username = username
        self.roles = roles
        self.roles_links = roles_links

    @classmethod
    def _dict_to_obj(cls, data):
        return cls(
            id_=data.get('id'),
            name=data.get('name'),
            username=data.get('username'),
            roles=RolesList._dict_to_obj(data.get('roles')),
            roles_links=RolesLinks._dict_to_obj(data.get('roles_links')))

    @classmethod
    def _xml_ele_to_obj(cls, ele):
        return cls(
            id_=ele.attrib.get('id'),
            name=ele.attrib.get('name'),
            username=ele.attrib.get('username'),
            roles=RolesList._xml_ele_to_obj(ele.findall('role')),
            roles_links=RolesLinks._xml_ele_to_obj(ele.find('roles_links')))


class Metadata(BaseIdentityModel):

    @classmethod
    def _dict_to_obj(cls, data):
        return data

    @classmethod
    def _xml_ele_to_obj(cls, ele):
        return ele.attrib


class Service(BaseIdentityModel):
    def __init__(
            self, endpoints=None, endpoints_links=None, name=None, type_=None):
        super(Service, self).__init__()

        self.endpoints = endpoints
        self.endpoints_links = endpoints_links
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
        return None

    @classmethod
    def _dict_to_obj(cls, data):
        return cls(
            endpoints=EndpointsList._dict_to_obj(data.get('endpoints')),
            endpoints_links=EndpointsLinks._dict_to_obj(
                data.get('endpoints_links')),
            name=data.get('name'), type_=data.get('type'))

    @classmethod
    def _xml_ele_to_obj(cls, ele):
        return cls(
            endpoints=EndpointsList._xml_ele_to_obj(ele.findall("endpoint")),
            endpoints_links=EndpointsLinks._xml_ele_to_obj(
                ele.find('endpoints_links')),
            name=ele.attrib.get('name'),
            type_=ele.attrib.get('type'))


class EndpointsLinks(BaseIdentityListModel):
    # always returns an empty list since no documentation on endpoint links
    @classmethod
    def _dict_to_obj(cls, data):
        return EndpointsLinks()

    @classmethod
    def _xml_ele_to_obj(cls, ele):
        return EndpointsLinks()


class EndpointsList(BaseIdentityListModel):

    @classmethod
    def _dict_to_obj(cls, data):
        return EndpointsList([Endpoint._dict_to_obj(obj) for obj in data])

    @classmethod
    def _xml_ele_to_obj(cls, ele):
        return EndpointsList([Endpoint._xml_ele_to_obj(obj) for obj in ele])


class Endpoint(BaseIdentityModel):
    def __init__(
            self, region=None, id_=None, public_url=None, admin_url=None,
            internal_url=None, private_url=None, version_id=None,
            version_info=None, version_list=None):
        super(Endpoint, self).__init__()

        self.region = region
        self.id_ = id_
        self.public_url = public_url
        self.admin_url = admin_url
        self.internal_url = internal_url
        self.private_url = private_url
        self.version_id = version_id
        self.version_info = version_info
        self.version_list = version_list

    @classmethod
    def _dict_to_obj(cls, data):
        return cls(region=data.get('region'),
                   id_=data.get('Id'),
                   public_url=data.get('publicURL'),
                   private_url=data.get('privateURL'),
                   admin_url=data.get('adminURL'),
                   internal_url=data.get('internalURL'),
                   version_id=data.get('versionId'),
                   version_info=data.get('versionInfo'),
                   version_list=data.get('versionList'))

    @classmethod
    def _xml_ele_to_obj(cls, ele):
        return cls(region=ele.attrib.get('region'),
                   id_=ele.attrib.get('Id'),
                   public_url=ele.attrib.get('publicURL'),
                   private_url=ele.attrib.get('privateURL'),
                   admin_url=ele.attrib.get('adminURL'),
                   internal_url=ele.attrib.get('internalURL'),
                   version_id=ele.attrib.get('versionId'),
                   version_info=ele.attrib.get('versionInfo'),
                   version_list=ele.attrib.get('versionList'))


class RolesLinks(BaseIdentityListModel):
    # always returns an empty list since no documentation on role links
    @classmethod
    def _dict_to_obj(cls, data):
        return RolesLinks()

    @classmethod
    def _xml_ele_to_obj(cls, data):
        return RolesLinks()


class RolesList(BaseIdentityListModel):

    @classmethod
    def _dict_to_obj(cls, data):
        return EndpointsList([Role._dict_to_obj(obj) for obj in data])

    @classmethod
    def _xml_ele_to_obj(cls, elements):
        return ServiceCatalog([Role._xml_ele_to_obj(ele) for ele in elements])


class ValidationResponseToken(BaseIdentityModel):
    def __init__(self, id_=None, expires=None, tenant=None):
        super(ValidationResponseToken, self).__init__()

        self.id_ = id_
        self.expires = expires
        self.tenant = tenant

    @classmethod
    def _dict_to_obj(cls, data):
        return cls(
            id_=data.get('id'), expires=data.get('expires'),
            tenant=ValidationResponseTenant._dict_to_obj(data.get('tenant')))

    @classmethod
    def _xml_ele_to_obj(cls, ele):
        return cls(
            id_=ele.attrib.get('id'), expires=ele.attrib.get('expires'),
            tenant=ValidationResponseTenant._xml_ele_to_obj(
                ele.find('tenant')))


class ValidationResponseTenant(BaseIdentityModel):
    def __init__(self, id_=None, name=None):
        super(ValidationResponseTenant, self).__init__()

        self.id_ = id_
        self.name = name

    @classmethod
    def _dict_to_obj(cls, data):
        return cls(id_=data.get('id'), name=data.get('name'))

    @classmethod
    def _xml_ele_to_obj(cls, ele):
        return cls(id_=ele.attrib.get('id'), name=ele.attrib.get('name'))


class ValidationResponseUser(BaseIdentityModel):
    def __init__(
            self, id_=None, name=None, roles=None, roles_links=None):
        super(ValidationResponseUser, self).__init__()
        self.id_ = id_
        self.name = name
        self.roles = roles
        self.roles_links = roles_links

    @classmethod
    def _dict_to_obj(cls, data):
        return cls(
            id_=data.get('id'), name=data.get('name'),
            roles=RolesList._dict_to_obj(data.get('roles')),
            roles_links=RolesLinks._dict_to_obj(data.get('roles_links')))

    @classmethod
    def _xml_ele_to_obj(cls, ele):
        return cls(
            id_=ele.attrib.get('id'), name=ele.attrib.get('name'),
            roles=RolesList._xml_ele_to_obj(ele.find('role')),
            roles_links=RolesLinks._dict_to_obj(ele.find('roles_links')))


class ValidationResponse(BaseIdentityModel):
    def __init__(self, token=None, user=None):
        super(ValidationResponse, self).__init__()
        self.token = token
        self.user = user

    @classmethod
    def _json_to_obj(cls, serialized_str):
        data_dict = json.loads(serialized_str)
        return cls._dict_to_obj(data_dict.get("access"))

    @classmethod
    def _dict_to_obj(cls, data):
        return cls(
            token=ValidationResponseToken._dict_to_obj(data.get('token')),
            user=ValidationResponseUser._dict_to_obj(data.get('user')))

    @classmethod
    def _xml_ele_to_obj(cls, ele):
        return cls(
            token=ValidationResponseToken._xml_ele_to_obj(ele.find('token')),
            user=ValidationResponseUser._xml_ele_to_obj(ele.find('user')))
