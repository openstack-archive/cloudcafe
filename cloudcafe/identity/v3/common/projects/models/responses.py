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

from cloudcafe.identity.common.models.base import (
    BaseIdentityModel)
from cloudcafe.identity.v3.common.domains.models.responses import Domain


class Project(BaseIdentityModel):
    """
    Response model for Project
    """

    def __init__(self, id_=None, name=None, domain=None):
        super(Project, self).__init__(locals())

    @classmethod
    def _dict_to_obj(cls, data):
        """
        @summary: Converting Dictionary Representation of a Project object
            to a Project object
        @return: Project object
        @param data: Dictionary Representation of a Project object
        """
        if 'domain' in data:
            data['domain'] = Domain._dict_to_obj(data.get("domain"))

        return cls(
            id_=data.get("id"),
            name=data.get("name"),
            domain=data.get("domain"))
