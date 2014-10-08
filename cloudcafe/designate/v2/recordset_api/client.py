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
from cloudcafe.designate.v2.recordset_api.models.requests import (
    RecordsetRequest)
from cloudcafe.designate.v2.recordset_api.models.responses import (
    RecordsetResponse, RecordsetListResponse)


class RecordsetAPIClient(DesignateClient):

    def __init__(self, url, serialize_format=None, deserialize_format=None):
        super(RecordsetAPIClient, self).__init__(url, serialize_format,
                                                 deserialize_format)

    def _get_recordsets_url(self, zone_id):
        return "{0}/zones/{1}/recordsets".format(self.url, zone_id)

    def _get_recordset_url(self, zone_id, recordset_id):
        return "{0}/{1}".format(self._get_recordsets_url(zone_id),
                                recordset_id)

    def create_recordset(self, zone_id, name=None, type=None, data=None, ttl=None,
                         **requestslib_kwargs):
        """POST /zones/{zoneID}/recordsets"""
        recordset_req = RecordsetRequest(name=name, data=data,
                                         type=type, ttl=ttl)
        url = self._get_recordsets_url(zone_id)

        return self.request('POST', url, request_entity=recordset_req,
                            response_entity_type=RecordsetResponse,
                            requestslib_kwargs=requestslib_kwargs)

    def list_recordsets(self, zone_id, **requestslib_kwargs):
        """GET /zones/{zoneID}/recordsets"""
        url = self._get_recordsets_url(zone_id)

        return self.request('GET', url,
                            response_entity_type=RecordsetListResponse,
                            requestslib_kwargs=requestslib_kwargs)

    def get_recordset(self, zone_id, recordset_id,
                       **requestslib_kwargs):
        """GET /zones/{zoneID}/recordsets/{recordsetID}"""
        url = self._get_recordset_url(zone_id, recordset_id)

        return self.request('GET', url,
                            response_entity_type=RecordsetResponse,
                            requestslib_kwargs=requestslib_kwargs)

    def update_recordset(self, zone_id, recordset_id=None, name=None,
                         type=None, data=None, **requestslib_kwargs):
        """PUT /zones/{zoneID}/recordsets/{recordsetID}"""
        recordset_req = RecordsetRequest(name=name, data=data, type=type)

        url = self._get_recordset_url(zone_id, recordset_id)

        return self.request('PUT', url,
                            response_entity_type=RecordsetResponse,
                            request_entity=recordset_req,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_recordset(self, zone_id, recordset_id, **requestslib_kwargs):
        """DELETE /zones/{zoneID}/recordsets/{recordsetID}"""
        url = self._get_recordset_url(zone_id, recordset_id)
        return self.request('DELETE', url)
