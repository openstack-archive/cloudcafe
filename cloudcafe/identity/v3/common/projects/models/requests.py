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
from cloudcafe.identity.v3.common.domains.models.requests import Domain


class Project(BaseIdentityModel):
    """
    Request model for v3 Project object
    """

    def __init__(self, id_=None, name=None, project_domain_name=None,
                 project_domain_id=None,):
        super(Project, self).__init__(locals())

        self.id_ = id_
        self.name = name
        self.project_domain_id = project_domain_id
        self.project_domain_name = project_domain_name
        self.domain = Domain(name=self.project_domain_name,
                             id_=self.project_domain_id)._obj_to_dict()

    def _obj_to_dict(self):
        """
        @summary: Converting Project object to a Dictionary representation
        @return: Dictionary representation of a Project object
        """
        ret = dict()
        if self.id_ is not None:
            ret['id'] = self.id_
        if self.name is not None:
            ret['name'] = self.name
        if self.project_domain_id is not None:
            ret['domain'] = dict(self.domain)
        if self.project_domain_name is not None:
            ret['domain'] = dict(self.domain)
        return self._remove_empty_values(ret)
