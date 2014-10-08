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
from cloudcafe.designate.v2.zone_api.models.requests import (
    ZoneRequest, ImportZoneRequest)
from cloudcafe.designate.v2.zone_api.models.responses import (
    ZoneResponse, ZoneListResponse, ExportZoneResponse)


class ZoneAPIClient(DesignateClient):

    def __init__(self, url, serialize_format=None, deserialize_format=None):
        super(ZoneAPIClient, self).__init__(url, serialize_format,
                                            deserialize_format)

    def _get_zones_url(self):
        return "{0}/zones".format(self.url)

    def _get_zone_url(self, zone_id):
        return "{0}/{1}".format(self._get_zones_url(), zone_id)

    def create_zone(self, name=None, email=None, ttl=None,
                    description=None, **requestslib_kwargs):
        """POST /zones"""
        zone_req = ZoneRequest(name=name, email=email, ttl=ttl,
                               description=description)
        url = self._get_zones_url()
        return self.request("POST", url, response_entity_type=ZoneResponse,
                            request_entity=zone_req,
                            requestslib_kwargs=requestslib_kwargs)

    def update_zone(self, name=None, zone_id=None, email=None,
                    ttl=None, description=None,
                    **requestslib_kwargs):
        """PATCH /zones/{zoneID}"""
        zone_req = ZoneRequest(name=name, email=email, ttl=ttl,
                               description=description)
        url = self._get_zone_url(zone_id)
        return self.request("PATCH", url, response_entity_type=ZoneResponse,
                            request_entity=zone_req,
                            requestslib_kwargs=requestslib_kwargs)

    def get_zone(self, zone_id, **requestslib_kwargs):
        """GET /zones/{zoneID}"""
        url = self._get_zone_url(zone_id)
        return self.request("GET", url, response_entity_type=ZoneResponse,
                            requestslib_kwargs=requestslib_kwargs)

    def list_zones(self, **requestslib_kwargs):
        """GET /zones"""
        url = self._get_zones_url()
        return self.request("GET", url, response_entity_type=ZoneListResponse,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_zone(self, zone_id, **requestslib_kwargs):
        """DELETE /zones/{zoneID}"""
        url = self._get_zone_url(zone_id)
        return self.request("DELETE", url, response_entity_type=ZoneResponse,
                            requestslib_kwargs=requestslib_kwargs)

    def export_zone(self, zone_id, **requestslib_kwargs):
        """GET /zones/{zoneID}"""
        headers = {"Accept": "text/dns"}
        url = self._get_zone_url(zone_id)
        return self.request("GET", url, headers=headers,
                            response_entity_type=ExportZoneResponse,
                            requestslib_kwargs=requestslib_kwargs)

    def import_zone(self, import_text, **requestslib_kwargs):
        """POST /zones"""
        headers = {"Content-Type": "text/dns"}
        url = self._get_zones_url()
        import_req = ImportZoneRequest(import_text=import_text)
        return self.request("POST", url, headers=headers,
                            request_entity=import_req,
                            response_entity_type=ZoneResponse,
                            requestslib_kwargs=requestslib_kwargs)
