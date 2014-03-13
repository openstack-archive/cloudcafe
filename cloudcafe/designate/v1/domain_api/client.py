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

from cafe.engine.clients.rest import AutoMarshallingRestClient
from cloudcafe.designate.v1.domain_api.models.requests import DomainRequest
from cloudcafe.designate.v1.domain_api.models.responses import (
    DomainResponse, DomainListResponse)


class DomainAPIClient(AutoMarshallingRestClient):

    def __init__(self, url, serialize_format=None,
                 deserialize_format=None):
        super(DomainApiClient, self).__init__(serialize_format,
                                              deserialize_format)
        self.url = url.rstrip('/')
        self.default_headers['Content-Type'] = 'application/{0}'.format(
            self.serialize_format)
        self.default_headers['Accept'] = 'application/{0}'.format(
            self.serialize_format)

    def _get_domains_url(self):
        return "{0}/domains".format(self.url)

    def _get_domain_url(self, domain_id):
        return "{0}/{1}".format(self._get_domains_url(), domain_id)

    def create_domain(self, name=None, email=None, ttl=None,
                      **requestslib_kwargs):
        """POST /domains"""
        domain_req = DomainRequest(name=name, email=email, ttl=ttl)
        url = self._get_domains_url()
        return self.request('POST', url, response_entity_type=DomainResponse,
                            request_entity=domain_req,
                            requestslib_kwargs=requestslib_kwargs)

    def update_domain(self, name=None, domain_id=None, email=None,
                      ttl=None, **requestslib_kwargs):
        """PUT /domains/{domainID}"""
        domain_req = DomainRequest(name=name, email=email, ttl=ttl)
        url = self._get_domain_url(domain_id)
        return self.request('PUT', url, response_entity_type=DomainResponse,
                            request_entity=domain_req,
                            requestslib_kwargs=requestslib_kwargs)

    def get_domain(self, domain_id, **requestslib_kwargs):
        """GET /domains/{domainID}"""
        url = self._get_domain_url(domain_id)
        return self.request('GET', url, response_entity_type=DomainResponse,
                            requestslib_kwargs=requestslib_kwargs)

    def list_domains(self, **requestslib_kwargs):
        """GET /domains"""
        url = self._get_domains_url()
        return self.request('GET', url,
                            response_entity_type=DomainListResponse,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_domain(self, domain_id, **requestslib_kwargs):
        """DELETE /domains/{domainID}"""
        url = self._get_domain_url(domain_id)
        return self.request('DELETE', url, response_entity_type=DomainResponse,
                            requestslib_kwargs=requestslib_kwargs)
