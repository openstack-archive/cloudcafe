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
import hmac
import json

from time import time
from hashlib import sha1
from cafe.engine.clients.rest import RestClient
from cloudcafe.objectstorage.objectstorage_api.models.responses \
    import AccountContainersList, ContainerObjectsList


def _deserialize(response_entity_type):
    """
    Auto-deserializes the response from any decorated client method call
    that has a 'format' key in it's 'params' dictionary argument, where
    'format' value is either 'json' or 'xml'.

    Deserializes the response into response_entity_type domain object

    response_entity_type must be a Domain Object with a <format>_to_obj()
    classmethod defined for every supported format or this won't work.
    """

    def decorator(f):
        def wrapper(*args, **kwargs):
            response = f(*args, **kwargs)
            response.request.__dict__['entity'] = None
            response.__dict__['entity'] = None
            deserialize_format = None
            if isinstance(kwargs, dict):
                if isinstance(kwargs.get('params'), dict):
                    deserialize_format = kwargs['params'].get('format')

            if deserialize_format is not None:
                response.__dict__['entity'] = \
                    response_entity_type.deserialize(
                        response.content, deserialize_format)
            return response
        return wrapper
    return decorator


class ObjectStorageAPIClient(RestClient):

    def __init__(self, storage_url, auth_token, base_container_name=None,
                 base_object_name=None):
        super(ObjectStorageAPIClient, self).__init__()
        self.storage_url = storage_url
        self.auth_token = auth_token
        self.base_container_name = base_container_name or ''
        self.base_object_name = base_object_name or ''
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
                meta_key = '{0}{1}'.format(prefix, key)
            except TypeError as e:
                self.client_log.error(
                    'Non-string prefix OR metadata dict value was passed '
                    'to __build_metadata() in object_client.py')
                self.client_log.exception(e)
                raise
            except:
                raise
            metadata_headers[meta_key] = metadata[key]

        return dict(metadata_headers, **headers)

    #Account-------------------------------------------------------------------

    def retrieve_account_metadata(self, requestslib_kwargs=None):
        """4.1.1 View Account Details"""
        response = self.head(
            self.storage_url,
            requestslib_kwargs=requestslib_kwargs)

        return response

    @_deserialize(AccountContainersList)
    def list_containers(self, headers=None, params=None,
                        requestslib_kwargs=None):
        """
        Lists all containers for the account.

        If the 'format' variable is passed as part of the 'params'
        dictionary, an object representing the deserialized version of
        that format (either xml or json) will be appended to the response
        as the 'entity' attribute. (ie, response.entity)
        """
        response = self.get(
            self.storage_url,
            headers=headers,
            params=params,
            requestslib_kwargs=requestslib_kwargs)

        return response

    #Container-----------------------------------------------------------------

    def get_container_metadata(self, container_name, headers=None,
                               requestslib_kwargs=None):
        """4.2.1 View Container Details"""
        url = '{0}/{1}'.format(self.storage_url, container_name)

        response = self.head(
            url,
            headers=headers,
            requestslib_kwargs=requestslib_kwargs)

        return response

    def create_container(self, container_name, metadata=None, headers=None,
                         requestslib_kwargs=None):
        url = '{0}/{1}'.format(self.storage_url, container_name)
        headers = self.__add_container_metadata_to_headers(metadata, headers)

        response = self.put(
            url,
            headers=headers,
            requestslib_kwargs=requestslib_kwargs)

        return response

    def update_container(self, container_name, headers=None,
                         requestslib_kwargs=None):
        url = '{0}/{1}'.format(self.storage_url, container_name)

        response = self.put(
            url,
            headers=headers,
            requestslib_kwargs=requestslib_kwargs)

        return response

    def delete_container(self, container_name, headers=None,
                         requestslib_kwargs=None):
        url = '{0}/{1}'.format(self.storage_url, container_name)

        response = self.delete(
            url,
            headers=headers,
            requestslib_kwargs=requestslib_kwargs)

        return response

    def set_container_metadata(self, container_name, metadata, headers=None,
                               requestslib_kwargs=None):
        url = '{0}/{1}'.format(self.storage_url, container_name)
        headers = self.__add_container_metadata_to_headers(metadata, headers)

        response = self.post(
            url,
            headers=headers,
            requestslib_kwargs=requestslib_kwargs)

        return response

    def get_container_options(self, container_name, headers=None,
                              requestslib_kwargs=None):
        """4.2.5 CORS Container Headers"""
        url = '{0}/{1}'.format(self.storage_url, container_name)

        response = self.options(
            url,
            headers=headers,
            requestslib_kwargs=requestslib_kwargs)

        return response

    @_deserialize(ContainerObjectsList)
    def list_objects(self, container_name, headers=None, params=None,
                     requestslib_kwargs=None):
        """
        Lists all objects in the specified container.

        If the 'format' variable is passed as part of the 'params'
        dictionary, an object representing the deserialized version of
        that format (either xml or json) will be appended to the response
        as the 'entity' attribute. (ie, response.entity)
        """
        url = '{0}/{1}'.format(self.storage_url, container_name)

        response = self.get(
            url,
            headers=headers,
            params=params,
            requestslib_kwargs=requestslib_kwargs)

        return response

    def get_object_count(self, container_name):
        """
        Returns the number of objects in a container.
        """
        response = self.get_container_metadata(container_name)

        obj_count = int(response.headers['x-container-object-count'])

        return obj_count

    def _purge_container(self, container_name):
        params = {'format': 'json'}
        response = self.list_objects(container_name, params=params)
        try:
            json_data = json.loads(response.content)
            for entry in json_data:
                self.delete_object(container_name, entry['name'])
        except Exception:
            pass

        return self.delete_container(container_name)

    def force_delete_containers(self, container_list):
        for container_name in container_list:
            return self._purge_container(container_name)

    #Storage Object------------------------------------------------------------

    def get_object(self, container_name, object_name, headers=None,
                   prefetch=True, requestslib_kwargs=None):
        """
        optional headers

        If-Match
        If-None-Match
        If-Modified-Since
        If-Unmodified-Since
        Range

        If-Match and If-None-Match check the ETag header
        200 on 'If' header success
        If none of the entity tags match, or if "*" is given and no current
        entity exists, the server MUST NOT perform the requested method, and
        MUST return a 412 (Precondition Failed) response.

        206 (Partial content) for successful range request
        If the entity tag does not match, then the server SHOULD
        return the entire entity using a 200 (OK) response
        see RFC2616

        If prefetch=False, body download is delayed until response.content is
        accessed either directly, via response.iter_content() or .iter_lines()
        """
        url = '{0}/{1}/{2}'.format(
            self.storage_url,
            container_name,
            object_name)

        if requestslib_kwargs is None:
            requestslib_kwargs = {}

        if requestslib_kwargs.get('prefetch') is None:
            requestslib_kwargs['prefetch'] = prefetch

        response = self.get(
            url,
            headers=headers,
            requestslib_kwargs=requestslib_kwargs)

        return response

    def create_object(self, container_name, object_name, data=None,
                      metadata=None, headers=None, requestslib_kwargs=None):
        """
        Creates a storage object in a container via PUT
        Optionally adds 'X-Object-Metadata-' prefix to any key in the
        metadata dictionary, and then adds that metadata to the headers
        dictionary.
        """
        url = '{0}/{1}/{2}'.format(
            self.storage_url,
            container_name,
            object_name)
        hdrs = self.__add_object_metadata_to_headers(metadata, headers)

        response = self.put(
            url,
            headers=hdrs,
            data=data,
            requestslib_kwargs=requestslib_kwargs)

        return response

    def copy_object(self, container_name, object_name, headers=None):
        url = '{0}/{1}/{2}'.format(
            self.storage_url,
            container_name,
            object_name)
        hdrs = {}
        hdrs['X-Auth-Token'] = self.auth_token

        if headers is not None:
            if 'X-Copy-From' in headers and 'Content-Length' in headers:
                method = 'PUT'
                hdrs['X-Copy-From'] = headers['X-Copy-From']
                hdrs['Content-Length'] = headers['Content-Length']
            elif 'Destination' in headers:
                method = 'COPY'
                hdrs['Destination'] = headers['Destination']
            else:
                return None

        response = self.request(method=method, url=url, headers=hdrs)

        return response

    def delete_object(self, container_name, object_name, headers=None,
                      requestslib_kwargs=None):
        url = '{0}/{1}/{2}'.format(
            self.storage_url,
            container_name,
            object_name)

        response = self.delete(
            url,
            headers=headers,
            requestslib_kwargs=requestslib_kwargs)

        return response

    def get_object_metadata(self, container_name, object_name,
                            headers=None, requestslib_kwargs=None):
        url = '{0}/{1}/{2}'.format(
            self.storage_url,
            container_name,
            object_name)

        response = self.head(
            url,
            headers=headers,
            requestslib_kwargs=requestslib_kwargs)

        return response

    def set_object_metadata(self, container_name, object_name, metadata,
                            headers=None, requestslib_kwargs=None):
        url = '{0}/{1}/{2}'.format(
            self.storage_url,
            container_name,
            object_name)
        headers = self.__add_object_metadata_to_headers(metadata, headers)

        response = self.post(
            url,
            headers=headers,
            requestslib_kwargs=requestslib_kwargs)

        return response

    def set_temp_url_key(self, headers=None, requestslib_kwargs=None):
        return self.post(self.storage_url, headers=headers)

    def create_temp_url(self, method, container, obj, seconds, key,
                        headers=None, requestslib_kwargs=None):
        method = method.upper()
        base_url = '{0}/{1}/{2}'.format(self.storage_url, container, obj)
        account_hash = self.storage_url.split('/v1/')[1]
        object_path = '/v1/{0}/{1}/{2}'.format(account_hash, container, obj)
        seconds = int(seconds)
        expires = int(time() + seconds)
        hmac_body = '{0}\n{1}\n{2}'.format(method, expires, object_path)
        sig = hmac.new(key, hmac_body, sha1).hexdigest()

        return {'target_url': base_url, 'signature': sig, 'expires': expires}
