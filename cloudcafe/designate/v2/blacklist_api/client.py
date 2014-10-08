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
from cloudcafe.designate.v2.blacklist_api.models.requests import (
    BlacklistRequest)
from cloudcafe.designate.v2.blacklist_api.models.responses import (
    BlacklistResponse, BlacklistListResponse)


class BlacklistAPIClient(DesignateClient):

    def __init__(self, url, serialize_format=None, deserialize_format=None):
        super(BlacklistAPIClient, self).__init__(url, serialize_format,
                                              deserialize_format)

    def _get_blacklists_url(self):
        return "{0}/blacklists".format(self.url)

    def _get_blacklist_url(self, blacklist_id):
        return "{0}/{1}".format(self._get_blacklists_url(), blacklist_id)

    def create_blacklist(self, pattern=None, description=None,
                         **requestslib_kwargs):
        """POST /blacklists"""
        blacklist_req = BlacklistRequest(pattern=pattern,
                                         description=description)
        url = self._get_blacklists_url()
        return self.request('POST', url, request_entity=blacklist_req,
                            response_entity_type=BlacklistResponse,
                            requestslib_kwargs=requestslib_kwargs)

    def list_blacklists(self, **requestslib_kwargs):
        """GET /blacklists"""
        url = self._get_blacklists_url()
        return self.request('GET', url,
                            response_entity_type=BlacklistListResponse,
                            requestslib_kwargs=requestslib_kwargs)

    def get_blacklist(self, blacklist_id, **requestslib_kwargs):
        """GET /blacklists/{blacklistID}"""
        url = self._get_blacklist_url(blacklist_id)
        return self.request('GET', url, response_entity_type=BlacklistResponse,
                            requestslib_kwargs=requestslib_kwargs)

    def update_blacklist(self, pattern=None, description=None,
                         blacklist_id=None, **requestslib_kwargs):
        """PATCH /blacklists/{blacklistID}"""
        blacklist_req = BlacklistRequest(description=description,
                                         pattern=pattern)
        url = self._get_blacklist_url(blacklist_id)
        return self.request('PATCH', url, request_entity=blacklist_req,
                            response_entity_type=BlacklistResponse,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_blacklist(self, blacklist_id, **requestslib_kwargs):
        """DELETE /blacklists/{blacklistID}"""
        url = self._get_blacklist_url(blacklist_id)
        return self.request('DELETE', url,
                            requestslib_kwargs=requestslib_kwargs)
