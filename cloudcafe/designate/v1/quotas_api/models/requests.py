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

from cafe.engine.models.base import AutoMarshallingModel


class QuotasRequest(AutoMarshallingModel):

    def __init__(self, domains=None, recordset_records=None,
                 domain_records=None, domain_recordsets=None):
        self.domains = domains
        self.recordset_records = recordset_records
        self.domain_records = domain_records
        self.domain_recordsets = domain_recordsets

    def _obj_to_json(self):
        return json.dumps(self._obj_to_dict())

    def _obj_to_dict(self):
        return {"domain_records": self.domain_records,
                "domain_recordsets": self.domain_recordsets,
                "domains": self.domains,
                "recordset_records": self.recordset_records}
