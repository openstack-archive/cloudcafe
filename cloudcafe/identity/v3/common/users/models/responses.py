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
    BaseIdentityModel)
from cloudcafe.identity.v3.common.domains.models.responses import Domain


class User(BaseIdentityModel):
    """
    Response model for User
    """

    NS_PREFIX = 'RAX-AUTH'

    def __init__(
            self, id_=None, name=None, domain=None,
            default_region=None, default_project_id=None):
        super(User, self).__init__(locals())

    @classmethod
    def _dict_to_obj(cls, data):
        """
        @summary: Converting Dictionary Representation of a User object
            to a User object
        @return: User object
        @param data: Dictionary Representation of a User object
        """
        if data is None:
            return None
        data = cls._remove_prefix(prefix=cls.NS_PREFIX, data_dict=data)
        if 'domain' in data:
            data['domain'] = Domain._dict_to_obj(data.get("domain"))

        return cls(
            id_=data.get("id"),
            name=data.get("name"),
            default_project_id=data.get("default_project_id"),
            default_region=data.get("default_region"),
            domain=data.get("domain"))
