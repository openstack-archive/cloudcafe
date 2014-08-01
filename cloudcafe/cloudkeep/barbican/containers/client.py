"""
Copyright 2014 Rackspace

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
from cloudcafe.cloudkeep.barbican.client import BarbicanRestClient
from cloudcafe.cloudkeep.barbican.containers.models.container import (
    Container, ContainerRef, ContainerGroup)


class ContainerClient(BarbicanRestClient):

    def __init__(self, url, api_version, token=None,
                 serialize_format=None, deserialize_format=None):
        super(ContainerClient, self).__init__(
            token=token, serialize_format=serialize_format,
            deserialize_format=deserialize_format)
        self.url = url
        self.api_version = api_version

    def _get_base_url(self):
        return '{base}/{api_version}/containers'.format(
            base=self.url,
            api_version=self.api_version)

    def create_container(self, name, container_type, secret_refs):
        """ Creates a Barbican container.

        :param name: Container name.
        :param container_type: Container type {generic|rsa|certificate}.
        :param secret_refs: Contains a list of SecretRef objects
        """
        remote_url = self._get_base_url()
        container = Container(name, container_type, secret_refs)

        return self.request('POST', remote_url, request_entity=container,
                            response_entity_type=ContainerRef)

    def get_container(self, container_ref):
        """ Retrieves a Barbican container via a HATOAS reference url. """
        return self.request('GET', container_ref,
                            response_entity_type=Container)

    def get_containers(self, limit=None, offset=None, ref=None):
        """ Retrieves a collection of Barbican containers

        :param limit: The maximum number of containers to retrieve.
        :param offset: Starting index of containers.
        """
        resp = self.request('GET',
                            ref or self._get_base_url(),
                            params={'limit': limit, 'offset': offset},
                            response_entity_type=ContainerGroup)
        return resp

    def delete_container(self, container_ref):
        """ Deletes a container based on a HATOAS reference url. """
        return self.request('DELETE', container_ref)
