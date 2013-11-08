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

from cafe.engine.config import EngineConfig
from time import time
from hashlib import sha1
from cafe.engine.clients.rest import RestClient
from cloudcafe.objectstorage.objectstorage_api.models.responses \
    import AccountContainersList, ContainerObjectsList


def _deserialize(response_entity_type):
    """
    Auto-deserializes the response from any decorated client method call
    that has either a 'format' key in it's 'params' dictionary argument or an
    'accept' in it's 'headers' dictionary argument, where
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
                    lower_params = \
                        dict((key.lower(), value.lower()) for key, value in
                             kwargs['params'].iteritems())
                    deserialize_format = lower_params.get('format')
                elif isinstance(kwargs.get('headers'), dict):
                    lower_headers = \
                        dict((key.lower(), value.lower()) for key, value in
                             kwargs['headers'].iteritems())
                    deserialize_format = \
                        lower_headers.get('accept').split('/')[1]

            if deserialize_format:
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
        self.engine_config = EngineConfig()
        self.storage_url = storage_url
        self.auth_token = auth_token
        self.base_container_name = base_container_name or ''
        self.base_object_name = base_object_name or ''
        self.default_headers['X-Auth-Token'] = self.auth_token

    #Account-------------------------------------------------------------------

    def retrieve_account_metadata(self):
        response = self.head(self.storage_url)

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
        url = '{0}/{1}'.format(self.storage_url, container_name)

        response = self.head(
            url,
            headers=headers,
            requestslib_kwargs=requestslib_kwargs)

        return response

    def create_container(self, container_name, headers=None,
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

    def set_container_metadata(self, container_name, headers=None,
                               requestslib_kwargs=None):
        url = '{0}/{1}'.format(self.storage_url, container_name)

        response = self.post(
            url,
            headers=headers,
            requestslib_kwargs=requestslib_kwargs)

        return response

    def get_container_options(self, container_name, headers=None,
                              requestslib_kwargs=None):
        """
        returns response from CORS option call
        """
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

    def get_object_count(self, container_name,
                         requestslib_kwargs=None):
        """
        Returns the number of objects in a container.
        """
        response = self.get_container_metadata(
            container_name,
            requestslib_kwargs=requestslib_kwargs)

        obj_count = int(response.headers.get('x-container-object-count'))

        return obj_count

    def _purge_container(self, container_name,
                         requestslib_kwargs=None):
        params = {'format': 'json'}
        response = self.list_objects(
            container_name,
            params=params,
            requestslib_kwargs=requestslib_kwargs)

        try:
            json_data = json.loads(response.content)
            for entry in json_data:
                self.delete_object(container_name, entry['name'])
        except ValueError:
            pass

        return self.delete_container(container_name)

    def force_delete_containers(self, container_list,
                                requestslib_kwargs=None):
        for container_name in container_list:
            return self._purge_container(
                container_name,
                requestslib_kwargs=requestslib_kwargs)

    #Storage Object------------------------------------------------------------

    def get_object(self, container_name, object_name, headers=None,
                   params=None, stream=False,
                   requestslib_kwargs=None):
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

        response = self.get(
            url,
            headers=headers,
            params=params,
            requestslib_kwargs={'stream': stream})

        return response

    def create_object(self, container_name, object_name, data=None,
                      headers=None, params=None,
                      requestslib_kwargs=None):
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

        response = self.put(
            url,
            data=data,
            headers=headers,
            params=params,
            requestslib_kwargs=requestslib_kwargs)

        return response

    def copy_object(self, container_name, object_name, headers=None,
                    requestslib_kwargs=None):
        url = '{0}/{1}/{2}'.format(
            self.storage_url,
            container_name,
            object_name)

        if 'X-Copy-From' in headers:
            method = 'PUT'
            if 'Content-Length' not in headers:
                headers['Content-Length'] = '0'
        elif 'Destination' in headers:
            method = 'COPY'
        else:
            return None

        response = self.request(
            method=method,
            url=url,
            headers=headers,
            requestslib_kwargs=requestslib_kwargs)

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

    def get_object_metadata(self, container_name, object_name, headers=None,
                            requestslib_kwargs=None):
        url = '{0}/{1}/{2}'.format(
            self.storage_url,
            container_name,
            object_name)

        response = self.head(
            url,
            headers=headers,
            requestslib_kwargs=requestslib_kwargs)

        return response

    def set_object_metadata(self, container_name, object_name, headers=None,
                            requestslib_kwargs=None):
        url = '{0}/{1}/{2}'.format(
            self.storage_url,
            container_name,
            object_name)

        response = self.post(
            url,
            headers=headers,
            requestslib_kwargs=requestslib_kwargs)

        return response

    def set_temp_url_key(self, headers=None,
                         requestslib_kwargs=None):
        response = self.post(
            self.storage_url,
            headers=headers,
            requestslib_kwargs=requestslib_kwargs)

        return response

    def create_temp_url(self, method, container, obj, seconds, key):
        method = method.upper()
        base_url = '{0}/{1}/{2}'.format(self.storage_url, container, obj)
        account_hash = self.storage_url.split('/v1/')[1]
        object_path = '/v1/{0}/{1}/{2}'.format(account_hash, container, obj)
        seconds = int(seconds)
        expires = int(time() + seconds)
        hmac_body = '{0}\n{1}\n{2}'.format(method, expires, object_path)
        sig = hmac.new(key, hmac_body, sha1).hexdigest()

        return {'target_url': base_url, 'signature': sig, 'expires': expires}
