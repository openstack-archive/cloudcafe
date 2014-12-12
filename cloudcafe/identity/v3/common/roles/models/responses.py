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

from cloudcafe.identity.v3.common.models.base import (
    BaseIdentityModel, BaseIdentityListModel)


class Roles(BaseIdentityListModel):
    """
    Response Model for Roles
    """

    @classmethod
    def _xml_ele_to_obj(cls, elements):
        return Roles(
            [Role._xml_ele_to_obj(element) for element in elements])

    @classmethod
    def _dict_to_obj(cls, data):
        """
        @summary: Converting Dictionary Representation of Roles object
            to Roles object
        @return: Roles object
        @param data: Dictionary Representation of Roles object
        """
        roles = cls()
        for user in data:
            roles.append(Role._dict_to_obj(user))
        return roles


class Role(BaseIdentityModel):
    """
    Response Model for a Role
    """

    NS_PREFIX = 'RAX-AUTH'

    def __init__(
            self, id_=None, name=None, tenant_id=None):
        super(Role, self).__init__(locals())

    @classmethod
    def _xml_ele_to_obj(cls, element):
        if element is None:
            return None
        return cls(
            id_=element.attrib.get("id"),
            name=element.attrib.get("name"))

    @classmethod
    def _dict_to_obj(cls, data):
        """
        @summary: Converting Dictionary Representation of a Role object
            to a Role object
        @return: Role object
        @param data: Dictionary Representation of a Role object
        """
        if data is None:
            return None
        data = cls._remove_prefix(prefix=cls.NS_PREFIX, data_dict=data)
        return cls(
            id_=data.get("id"), name=data.get("name"),
            tenant_id=data.get("tenant_id"))
