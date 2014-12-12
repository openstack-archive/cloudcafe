"""
Copyright 2014 Rackspace
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

from cloudcafe.identity.v3.common.models.base import BaseIdentityModel

from cloudcafe.identity.v3.common.roles.models.responses import Roles
from cloudcafe.identity.v3.common.catalog.models.responses import Catalog
from cloudcafe.identity.v3.common.users.models.responses import User
from cloudcafe.identity.v3.common.projects.models.responses import Project


class AuthResponse(BaseIdentityModel):
    """
    Auth Response model
    """

    ROOT_TAG = 'token'

    def __init__(
            self, token=None, roles=None, catalog=None, user=None,
            issued_at=None, extras=None, methods=None, project=None,
            expires_at=None):
        super(AuthResponse, self).__init__(locals())

    @classmethod
    def _dict_to_obj(cls, data):
        """
        @summary: Converting Dictionary Representation of AuthResponse object
            to AuthResponse object
        @return: AuthResponse object
        @param data: Dictionary Representation of AuthResponse object
        """
        if data is None:
            return None
        return cls(
            token=AuthResponseToken._dict_to_obj(data.get("token")),
            roles=Roles._dict_to_obj(data.get("roles") or []),
            user=User._dict_to_obj(data.get("user")),
            catalog=Catalog._dict_to_obj(data.get("catalog")) or [],
            issued_at=data.get("issued_at"),
            extras=data.get("extras"),
            methods=data.get("methods"),
            project=Project._dict_to_obj(data.get("project")),
            expires_at=data.get("expires_at"))

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """
        @summary: Converting JSON Representation of AuthResponse object
            to AuthResponse object
        @return: AuthResponse object
        @param serialized_str: JSON Representation of AuthResponse object
        """
        data = json.loads(serialized_str)
        return cls._dict_to_obj(data.get("access"))

    def get_service(self, name):
        if self.catalog:
            for service in self.catalog:
                if service.name == name:
                    return service
        return None


class AuthResponseToken(BaseIdentityModel):
    """
    Auth Response Token model
    """

    ID = "id"
    EXPIRES = "expires"
    TENANT = "tenant"
    AUTH_BY = "RAX-AUTH:authenticatedBy"

    def __init__(self, token_id=None, expires=None,
                 tenant=None, rax_auth_authenticated_by=None):
        self.token_id = token_id
        self.expires = expires
        self.tenant = tenant
        self.rax_auth_authenticated_by = rax_auth_authenticated_by

    @classmethod
    def _dict_to_obj(cls, data):
        """
        @summary: Converting Dictionary Representation of AuthResponseToken
         object to AuthResponseToken object
        @return: AuthResponseToken object
        @param data: Dictionary Representation of AuthResponseToken object
        """
        if data is None:
            return None
        return cls(token_id=data.get(cls.ID),
                   expires=data.get(cls.EXPIRES),
                   tenant=Tenant._dict_to_obj(data.get(cls.TENANT) or {}),
                   rax_auth_authenticated_by=data.get(cls.AUTH_BY))


class Tenant(BaseIdentityModel):
    """
    Model for Tenant
    """
    def __init__(self, name=None, id_=None):
        super(Tenant, self).__init__(locals())

    @classmethod
    def _xml_ele_to_obj(cls, element):
        if element is None:
            return None
        return cls(
            name=element.attrib.get("name"), id_=element.attrib.get("id"))

    @classmethod
    def _dict_to_obj(cls, data):
        """
        @summary: Converting Dictionary Representation of Tenant
         object to Tenant object
        @return: Tenant object
        @param data: Dictionary Representation of Tenant object
        """
        if data is None:
            return None
        return cls(
            name=data.get("name"), id_=data.get("id"))

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """
        @summary: Converting JSON Representation of Tenant object
            to Tenant object
        @return: Tenant object
        @param serialized_str: JSON Representation of Tenant object
        """
        data = json.loads(serialized_str)
        return cls._dict_to_obj(data.get("tenant"))
