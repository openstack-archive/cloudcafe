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
from cloudcafe.designate.v2.tld_api.models.requests import TLDRequest
from cloudcafe.designate.v2.tld_api.models.responses import (
    TLDResponse, TLDListResponse)


class TLDClient(DesignateClient):

    def __init__(self, url, serialize_format=None, deserialize_format=None):
        super(TLDClient, self).__init__(url, serialize_format,
                                        deserialize_format)

    def _get_tlds_url(self):
        return "{0}/tlds".format(self.url)

    def _get_tld_url(self, tld_id):
        return "{0}/{1}".format(self._get_tlds_url(), tld_id)

    def create_tld(self, name=None, description=None, **requestslib_kwargs):
        """POST /tlds"""
        request_tld = TLDRequest(name=name, description=description)
        url = self._get_tlds_url()
        return self.request('POST', url, request_entity=request_tld,
                            response_entity_type=TLDResponse,
                            requestslib_kwargs=requestslib_kwargs)

    def list_tlds(self, **requestslib_kwargs):
        """GET /tlds"""
        url = self._get_tlds_url()
        return self.request('GET', url, response_entity_type=TLDListResponse,
                            requestslib_kwargs=requestslib_kwargs)

    def get_tld(self, tld_id, **requestslib_kwargs):
        """GET /tlds/{tldID}"""
        url = self._get_tld_url(tld_id)
        return self.request('GET', url, response_entity_type=TLDResponse,
                            requestslib_kwargs=requestslib_kwargs)

    def update_tld(self, name=None, description=None,
                   tld_id=None, **requestslib_kwargs):
        """PATCH /tlds/{tldID}"""
        request_tld = TLDRequest(name=name, description=description)
        url = self._get_tld_url(tld_id)
        return self.request('PATCH', url, request_entity=request_tld,
                            response_entity_type=TLDResponse,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_tld(self, tld_id, **requestslib_kwargs):
        """DELETE /tlds/{tldID}"""
        url = self._get_tld_url(tld_id)
        return self.request('DELETE', url,
                            requestslib_kwargs=requestslib_kwargs)
