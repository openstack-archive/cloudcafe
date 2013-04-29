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

from urlparse import urlparse

from cafe.engine.clients.rest import AutoMarshallingRestClient
from cloudcafe.compute.flavors_api.models.flavor import \
    Flavor, FlavorMin, CreateFlavor


class FlavorsClient(AutoMarshallingRestClient):

    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None):
        """
        @param url: Base URL for the compute service
        @type url: String
        @param auth_token: Auth token to be used for all requests
        @type auth_token: String
        @param serialize_format: Format for serializing requests
        @type serialize_format: String
        @param deserialize_format: Format for de-serializing responses
        @type deserialize_format: String
        """
        super(FlavorsClient, self).__init__(serialize_format,
                                            deserialize_format)
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        ct = ''.join(['application/', self.serialize_format])
        accept = ''.join(['application/', self.deserialize_format])
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept
        self.url = url

    def create_flavor(self, name=None, ram=None, vcpus=None,
                      disk=None, id=None, is_public=None,
                      requestslib_kwargs=None):

        request = CreateFlavor(name=name, ram=ram, vcpus=vcpus,
                               disk=disk, id=id, is_public=is_public)

        url = '%s/flavors' % self.url
        resp = self.request('POST', url,
                            response_entity_type=Flavor,
                            request_entity=request,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def delete_flavor(self, flavor_id, requestslib_kwargs=None):

        url = '%s/flavors/%s' % (self.url, flavor_id)
        resp = self.request('DELETE', url,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def list_flavors(self, min_disk=None, min_ram=None, marker=None,
                     limit=None, requestslib_kwargs=None):
        '''
        @summary: Returns a list of flavors
        @param min_disk: min Disk in GB, to filter by minimum disk size in GB
        @type min_disk: int
        @param min_ram: min ram in GB, to filter by minimum RAM size in MB
        @type min_disk: int
        @param marker: ID of last item in previous list (paginated collections)
        @type marker:C{str}
        @param limit: Sets page size
        @type limit: int
        @return: List of flavors filtered by params on success
        @rtype: C{list}
        '''

        url = '%s/flavors' % (self.url)

        params = {'minDisk': min_disk, 'minRam': min_ram, 'marker': marker,
                  'limit': limit}
        flavor_response = self.request('GET', url, params=params,
                                       response_entity_type=FlavorMin,
                                       requestslib_kwargs=requestslib_kwargs)
        return flavor_response

    def list_flavors_with_detail(self, min_disk=None, min_ram=None,
                                 marker=None, limit=None,
                                 requestslib_kwargs=None):
        '''
        @summary: Returns details from a list of flavors
        @param min_disk: min Disk in GB, to filter by minimum Disk size in MB
        @type min_disk:int
        @param min_ram: min ram in GB, to filter by minimum RAM size in MB
        @type min_Disk:int
        @param marker: ID of last item in previous list (paginated collections)
        @type marker:C{str}
        @param limit: Sets page size
        @type limit: int
        @return: Detail List of flavors filtered by params on success
        @rtype: C{list}
        '''

        url = '%s/flavors/detail' % (self.url)

        params = {'minDisk': min_disk, 'minRam': min_ram, 'marker': marker,
                  'limit': limit}
        flavor_response = self.request('GET', url, params=params,
                                       response_entity_type=Flavor,
                                       requestslib_kwargs=requestslib_kwargs)
        return flavor_response

    def get_flavor_details(self, flavor_id, requestslib_kwargs=None):
        '''
        @summary: Returns a dict of details for given filter
        @param flavor_id: if of flavor for which details are required
        @type flavor_id:C{str}
        @return: Details of filter with filter id in the param on success
        @rtype: C{dict}
        '''

        url_new = str(flavor_id)
        url_scheme = urlparse(url_new).scheme
        url = url_new if url_scheme \
            else '%s/flavors/%s' % (self.url, flavor_id)

        flavor_response = self.request('GET', url, requestslib_kwargs,
                                       response_entity_type=Flavor,
                                       requestslib_kwargs=requestslib_kwargs)
        return flavor_response
