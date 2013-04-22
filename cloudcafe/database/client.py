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
from reddwarfclient import *
from reddwarfclient import xml


class DBaaSAPIClient(AutoMarshallingRestClient):
    """
    This class can be used to call directly into the REST API and
    wraps the python-reddwarfclient (so you can use that too)!

    """

    def __init__(self,
                 username,
                 url,
                 api_key,
                 auth_token,
                 tenant_id,
                 auth_url=None,
                 auth_strategy=None,
                 service_url=None,
                 insecure=False,
                 serialize_format=None,
                 deserialize_format=None):
        super(DBaaSAPIClient, self).__init__(serialize_format, deserialize_format)
        self.url = url
        self.tenant_id = tenant_id
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        self.default_headers['Content-Type'] = 'application/%s' % self.serialize_format
        self.default_headers['Accept'] = 'application/%s' % self.deserialize_format

        if self.serialize_format == 'xml':
            print "using the xml client!"
            self.reddwarfclient = Dbaas(username,
                                        api_key,
                                        tenant=tenant_id,
                                        auth_url=auth_url,
                                        client_cls=xml.ReddwarfXmlClient,
                                        service_url=service_url,
                                        auth_strategy=auth_strategy,
                                        insecure=insecure)
        else:
            self.reddwarfclient = Dbaas(username,
                                        api_key,
                                        tenant=tenant_id,
                                        auth_url=auth_url,
                                        service_url=service_url,
                                        auth_strategy=auth_strategy,
                                        insecure=insecure)

    def list_instances(self, requestslib_kwargs=None):

        url = '%s/%s/instances' % (self.url, self.tenant_id)

        return self.request('GET', url,
                            requestslib_kwargs=requestslib_kwargs)

    def create_instance(self, requestslib_kwargs=None):

        url = '%s/%s/instances' % (self.url, self.tenant_id)

        return self.request('POST', url,
                            requestslib_kwargs=requestslib_kwargs)

    def get_instance(self, instanceId, requestslib_kwargs=None):

        url = '%s/%s/instances/%s' % (self.url, self.tenant_id, instanceId)

        return self.request('GET', url,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_instance(self, instanceId, requestslib_kwargs=None):

        url = '%s/%s/instances/%s' % (self.url, self.tenant_id, instanceId)

        return self.request('DELETE', url,
                            requestslib_kwargs=requestslib_kwargs)

    def enable_root(self, instanceId, requestslib_kwargs=None):

        url = '%s/%s/instances/%s/root' % (self.url, self.tenant_id, instanceId)

        return self.request('POST', url,
                            requestslib_kwargs=requestslib_kwargs)
