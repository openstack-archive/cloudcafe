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

from cloudcafe.identity.common.models.base import BaseIdentityModel


class Domain(BaseIdentityModel):
    """
    Request model for v3 Domain object
    """

    ROOT_TAG = 'domain'

    def __init__(self, name=None, id_=None):
        super(Domain, self).__init__(locals())
        self.name = name
        self.id_ = id_

    def _obj_to_dict(self):
        """
        @summary: Converting Domain object to a Dictionary representation
        @return: Dictionary representation of a Domain object
        """
        ret = dict()
        if self.name is not None:
            ret['name'] = self.name
        if self.id_ is not None:
            ret['id'] = self.id_
        return self._remove_empty_values(ret)
