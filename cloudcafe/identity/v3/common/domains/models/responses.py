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


class Domain(BaseIdentityModel):
    """
    Response model for Domain
    """

    ROOT_TAG = 'domain'

    def __init__(self, id_=None, name=None):
        super(Domain, self).__init__(locals())

    @classmethod
    def _dict_to_obj(cls, data):
        """
        @summary: Converting Dictionary Representation of a Domain object
            to a Domain object
        @return: Domain object
        @param data: Dictionary Representation of a Domain object
        """
        if data is not None:
            return cls(
                id_=data.get("id"),
                name=data.get("name"))
