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

import cStringIO
import datetime
import json
import tarfile
import time
import urllib

from cafe.engine.clients.rest import RestClient


class ObjectStorageClient(RestClient):

    def __init__(self, storage_url, auth_token, base_container_name=None,
                 base_object_name=None):
        super(ObjectStorageClient, self).__init__()
        self.storage_url = storage_url
        self.auth_token = auth_token
        self.base_container_name = base_container_name
        self.base_object_name = base_object_name
        self.default_headers['X-Auth-Token'] = self.auth_token

    def __add_object_metadata_to_headers(self, metadata=None, headers=None):
        """
        Call to __build_metadata specifically for object headers
        """

        return self.__build_metadata('X-Object-Meta-', metadata, headers)

    def __add_container_metadata_to_headers(self, metadata=None, headers=None):
        """
        Call to __build_metadata specifically for container headers
        """

        return self.__build_metadata('X-Container-Meta-', metadata, headers)

    def __add_account_metadata_to_headers(self, metadata=None, headers=None):
        """
        Call to __build_metadata specifically for account headers
        """
        return self.__build_metadata('X-Account-Meta-', metadata, headers)

    def __build_metadata(self, prefix, metadata, headers):
        """
        Prepends the prefix to all keys in metadata dict, and then joins
        the metadata and header dictionaries together. When a conflict
        arises between two header keys, the key in headers wins over the
        key in metadata.

        Returns a dict composed of the provided headers and the new
        prefixed-metadata headers.

        @param prefix: Appended to all keys in metadata dict
        @type prefix: String
        @param metadata: Expects a dict with strings as keys and values
        @type metadata: Dict
        @rtype: Dict
        """
        if metadata is None:
            return headers

        headers = headers if headers is not None else {}
        metadata = metadata if metadata is not None else {}
        metadata_headers = {}

        for key in metadata:
            try:
                meta_key = ''.join([prefix, key])
            except TypeError as e:
                self.client_log.error(
                    'Non-string prefix OR metadata dict value was passed '
                    'to __build_metadata() in object_storage_client.py')
                self.client_log.exception(e)
                raise
            except:
                raise
            metadata_headers[meta_key] = metadata[key]

        return dict(metadata_headers, **headers)

    def create_container(self, container_name, metadata=None, headers=None,
                         requestslib_kwargs=None):

        headers = self.__add_container_metadata_to_headers(metadata, headers)

        url = '{0}/{1}'.format(self.storage_url, container_name)

        response = self.request(
                'PUT',
                url,
                headers=headers,
                requestslib_kwargs=requestslib_kwargs)

        return response

    def create_storage_object(self, container_name, object_name, data=None,
                              metadata=None, headers=None,
                              requestslib_kwargs=None):
        """
        Creates a storage object in a container via PUT
        Optionally adds 'X-Object-Metadata-' prefix to any key in the
        metadata dictionary, and then adds that metadata to the headers
        dictionary.
        """
        headers = self.__add_object_metadata_to_headers(metadata, headers)

        url = '{0}/{1}/{2}'.format(
                self.storage_url,
                container_name,
                object_name)

        response = self.request(
                'PUT',
                url,
                headers=headers,
                data=data,
                requestslib_kwargs=requestslib_kwargs)

        return response

    def delete_container(self, container_name, headers=None,
                         requestslib_kwargs=None):

        url = '{0}/{1}'.format(self.storage_url, container_name)

        response = self.request(
                'DELETE',
                url,
                headers=headers,
                requestslib_kwargs=requestslib_kwargs)

        return response

    def delete_storage_object(self, container_name, object_name, headers=None,
                              requestslib_kwargs=None):

        url = '{0}/{1}/{2}'.format(
                self.storage_url,
                container_name,
                object_name)

        response = self.request(
                'DELETE',
                url,
                headers=headers,
                requestslib_kwargs=requestslib_kwargs)

        return response

    def _purge_container(self, container_name):
        params = {'format': 'json'}
        r = self.list_objects(container_name, params=params)
        try:
            json_data = json.loads(r.content)
            for entry in json_data:
                self.delete_storage_object(container_name, entry['name'])
        except Exception:
            pass

        return self.delete_container(container_name)

    def force_delete_containers(self, container_list):
        for container_name in container_list:
            return self._purge_container(container_name)
