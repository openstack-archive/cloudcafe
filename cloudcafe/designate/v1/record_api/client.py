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
from cloudcafe.designate.v1.record_api.models.requests import RecordRequest
from cloudcafe.designate.v1.record_api.models.responses import (
    RecordResponse, RecordListResponse)


class RecordsAPIClient(DesignateClient):

    def __init__(self, url, serialize_format=None,
                 deserialize_format=None):
        super(RecordsAPIClient, self).__init__(url, serialize_format,
                                               deserialize_format)

    def _get_domain_url(self, domain_id):
        return "{0}/domains/{1}".format(self.url, domain_id)

    def _get_records_url(self, domain_id):
        return "{0}/records".format(self._get_domain_url(domain_id))

    def _get_record_url(self, domain_id, record_id):
        return "{0}/{1}".format(self._get_records_url(domain_id), record_id)

    def create_record(self, name=None, type=None,
                      data=None, priority=None,
                      domain_id=None, requestslib_kwargs=None):
        """POST /domains/{domainID}/records"""
        record_req = RecordRequest(name=name, data=data, record_type=type,
                                   priority=priority)
        url = self._get_records_url(domain_id)
        return self.request('POST', url, request_entity=record_req,
                            response_entity_type=RecordResponse,
                            requestslib_kwargs=requestslib_kwargs)

    def list_records(self, domain_id, requestslib_kwargs=None):
        """GET /domains/{domainID}/records"""
        url = self._get_records_url(domain_id)
        return self.request('GET', url,
                            response_entity_type=RecordListResponse,
                            requestslib_kwargs=requestslib_kwargs)

    def get_record(self, domain_id, record_id, requestslib_kwargs=None):
        """GET /domains/{domainID}/records/{recordID}"""
        url = self._get_record_url(domain_id, record_id)
        return self.request('GET', url, response_entity_type=RecordResponse,
                            requestslib_kwargs=requestslib_kwargs)

    def update_record(self, domain_id=None, name=None, type=None, data=None,
                      priority=None, record_id=None, requestslib_kwargs=None):
        """PUT /domains/{domainID}/records/{record_id}"""
        record_req = RecordRequest(name=name, data=data,
                                   record_type=type, priority=priority)
        url = self._get_record_url(domain_id, record_id)
        return self.request('PUT', url,
                            response_entity_type=RecordResponse,
                            request_entity=record_req,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_record(self, domain_id, record_id, requestslib_kwargs=None):
        """DELETE /domains/{domainID}/records/{recordID}"""
        url = self._get_record_url(domain_id, record_id)
        return self.request('DELETE', url,
                            response_entity_type=RecordResponse,
                            requestslib_kwargs=requestslib_kwargs)
