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

from cloudcafe.designate.client import DesignateClient
from cloudcafe.designate.v1.quotas_api.models.requests import QuotasRequest
from cloudcafe.designate.v1.quotas_api.models.responses import QuotasResponse


class QuotasAPIClient(DesignateClient):

    def __init__(self, url, serialize_format=None, deserialize_format=None):
        super(QuotasAPIClient, self).__init__(url, serialize_format,
                                              deserialize_format)

    def _get_quotas_url(self):
        return "{0}/quotas".format(self.url)

    def _get_quota_url(self, tenant_id):
        return "{0}/{1}".format(self._get_quotas_url(), tenant_id)

    def update_quotas(self, tenant_id=None, domains=None,
                      recordset_records=None, domain_records=None,
                      domain_recordsets=None, **requestslib_kwargs):
        """PUT /quotas/{tenantID}"""
        quota_req = QuotasRequest(domains=domains,
                                  recordset_records=recordset_records,
                                  domain_records=domain_records,
                                  domain_recordsets=domain_recordsets)
        url = self._get_quota_url(tenant_id)
        return self.request('PUT', url, response_entity_type=QuotasResponse,
                            request_entity=quota_req,
                            requestslib_kwargs=requestslib_kwargs)

    def get_quotas(self, tenant_id, **requestslib_kwargs):
        """GET /quotas/{tenantID}"""
        url = self._get_quota_url(tenant_id)
        return self.request('GET', url, response_entity_type=QuotasResponse,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_quotas(self, tenant_id, **requestslib_kwargs):
        """DELETE /quotas/{tenantID}"""
        url = self._get_quota_url(tenant_id)
        return self.request('DELETE', url, response_entity_type=QuotasResponse,
                            requestslib_kwargs=requestslib_kwargs)
