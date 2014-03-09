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
import tarfile
from time import sleep

from os.path import expanduser
from cloudcafe.common.tools import randomstring as randstring
from cafe.engine.config import EngineConfig
from cStringIO import StringIO
from time import time, mktime
from hashlib import sha1
from datetime import datetime, timedelta
from cloudcafe.common.tools.md5hash import get_md5_hash
from cafe.engine.http.client import HTTPClient
from cloudcafe.objectstorage.objectstorage_api.models.responses \
    import AccountContainersList, ContainerObjectsList, CreateArchiveObject


def _deserialize(response_entity_type):
    """
    Auto-deserializes the response from any decorated client method call.

    Deserializes the response into response_entity_type domain object

    response_entity_type must be a Domain Object with a <format>_to_obj()
    classmethod defined for every supported format or this won't work.
    """

    def decorator(f):
        def wrapper(*args, **kwargs):
            response = f(*args, **kwargs)
            setattr(response.request, 'entity', None)
            setattr(response, 'entity', None)
            deserialize_format = None

            content_type = response.headers.get('content-type', '')

            formats = ['text', 'json', 'xml']
            for format_ in formats:
                if format_ in content_type:
                    deserialize_format = format_
                    break

            resp_entity = response_entity_type.deserialize(
                response.content,
                deserialize_format)

            setattr(response, 'entity', resp_entity)

            return response
        return wrapper
    return decorator

BULK_ARCHIVE_NAME = 'bulk_objects'


class ObjectStorageAPIClientException(Exception):
    pass


class ObjectStorageAPIClient(HTTPClient):

    def __init__(self, storage_url, auth_token, base_container_name=None,
                 base_object_name=None, list_timeout=None):
        super(ObjectStorageAPIClient, self).__init__()
        self.engine_config = EngineConfig()
        self.temp_dir = expanduser(self.engine_config.temp_directory)
        self.swift_endpoint = storage_url.split('/v1/')[0]
        self.storage_url = storage_url
        self.auth_token = auth_token
        self.base_container_name = base_container_name or ''
        self.base_object_name = base_object_name or ''
        self.default_headers['X-Auth-Token'] = self.auth_token
        self._swift_features = None
        self.list_timeout = list_timeout

    def get_swift_info(self):
        """
        Returns a dictionary of info requested from swift.
        """
        info_url = '{0}/info'.format(self.swift_endpoint)
        return self.get(info_url)

    def _eventually_consistent(self, func, func_args=None, func_kwargs=None,
                               success_func=None, timeout=None):
        """
        Allows a function to be re-executed if a success condition is not met.
        The function will be called repeatedly, exponentially backing off until
        a timeout is met.  This mechanism ensures that eventual consistency
        does not interfere with test results.

        @param func: The function to be called and tested.
        @type func: function
        @param func_args: arguments to be passed to the function call.
        @type func_args: list
        @param func_kwargs: keyword arguments to be passed to the function
                            call.
        @type func_kwargs: dictionary
        @param success_func: A function that can optionally be provided
                                 for testing if the function call was
                                 successful or not.  This function would
                                 take the response object as an argument
                                 and return True if it was successful or
                                 False otherwise.  If a success function
                                 is not provided, it will default to checking
                                 response.ok.
        @type success_func: function
        @param timeout: Perform no more than one function call once the
                        timeout in seconds has elapsed since the first call.
                        If timeout is not provided, the function will only
                        be called once.
        @type timeout: int

        @return: The most resent response from calling func.
        @rtype: Response Object
        """
        sleep_seconds = 0
        func_args = func_args or []
        func_kwargs = func_kwargs or {}

        if self.list_timeout:
            stop_time = datetime.now() + timedelta(seconds=timeout)

        def default_success_func(response):
            return response.ok
        success_func = success_func or default_success_func

        response = None
        reached_success = False
        reached_timeout = False
        while not reached_success and not reached_timeout:
            if not timeout:
                reached_timeout = True
            else:
                reached_timeout = datetime.now() >= stop_time

            if sleep_seconds == 0:
                sleep_seconds = 1
            else:
                sleep(sleep_seconds)
                sleep_seconds = sleep_seconds * 2

            response = func(*func_args, **func_kwargs)

            if response is not None:
                reached_success = success_func(response)
            else:
                raise ObjectStorageAPIClientException('invalid response')

        return response

    #Account-------------------------------------------------------------------

    def retrieve_account_metadata(self):
        response = self.head(self.storage_url)

        return response

    @_deserialize(AccountContainersList)
    def _list_containers(self, headers=None, params=None,
                         requestslib_kwargs=None):
        """
        Lists all containers for the account.

        If the 'format' variable is passed as part of the 'params'
        dictionary, an object representing the deserialized version of
        that format (either xml or json) will be appended to the response
        as the 'entity' attribute. (ie, response.entity)

        @param headers: headers to be added to the HTTP request.
        @type headers: dictionary
        @param params: query string parameters to be added to the HTTP request.
        @type params: dictionary
        @param requestslib_kwargs: keyword arguments to be passed on to
                                   python requests.
        @type requestslib_kwargs: dictionary

        @return: response object
        @rtype: object
        """
        response = self.get(
            self.storage_url,
            headers=headers,
            params=params,
            requestslib_kwargs=requestslib_kwargs)

        return response

    def list_containers(self, headers=None, params=None,
                        requestslib_kwargs=None, success_func=None):
        """
        Eventually consistent version of _list_containers method.

        @param headers: headers to be added to the HTTP request.
        @type headers: dictionary
        @param params: query string parameters to be added to the HTTP request.
        @type params: dictionary
        @param requestslib_kwargs: keyword arguments to be passed on to
                                   python requests.
        @type requestslib_kwargs: dictionary
        @param success_func: used to test if a request was successful.
        @type success_func: function

        @return: response object
        @rtype: object
        """
        return self._eventually_consistent(
            self._list_containers,
            func_kwargs={
                'headers': headers,
                'params': params,
                'requestslib_kwargs': requestslib_kwargs},
            success_func=success_func,
            timeout=self.list_timeout)

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
    def _list_objects(self, container_name, headers=None, params=None,
                      requestslib_kwargs=None):
        """
        Lists all objects in the specified container.

        If the 'format' variable is passed as part of the 'params'
        dictionary, an object representing the deserialized version of
        that format (either xml or json) will be appended to the response
        as the 'entity' attribute. (ie, response.entity)

        @param container_name: container to list the object from.
        @type container_name: string
        @param headers: headers to be added to the HTTP request.
        @type headers: dictionary
        @param params: query string parameters to be added to the HTTP request.
        @type params: dictionary
        @param requestslib_kwargs: keyword arguments to be passed on to
                                   python requests.
        @type requestslib_kwargs: dictionary

        @return: response object
        @rtype: object
        """
        url = '{0}/{1}'.format(self.storage_url, container_name)

        response = self.get(
            url,
            headers=headers,
            params=params,
            requestslib_kwargs=requestslib_kwargs)

        return response

    def list_objects(self, container_name, headers=None, params=None,
                     requestslib_kwargs=None, success_func=None):
        """
        Eventually consistent version of _list_objects method.

        @param container_name: container to list the object from.
        @type container_name: string
        @param headers: headers to be added to the HTTP request.
        @type headers: dictionary
        @param params: query string parameters to be added to the HTTP request.
        @type params: dictionary
        @param requestslib_kwargs: keyword arguments to be passed on to
                                   python requests.
        @type requestslib_kwargs: dictionary
        @param success_func: used to test if a request was successful.
        @type success_func: function

        @return: response object
        @rtype: object
        """
        return self._eventually_consistent(
            self._list_objects,
            func_args=[container_name],
            func_kwargs={
                'headers': headers,
                'params': params,
                'requestslib_kwargs': requestslib_kwargs},
            success_func=success_func,
            timeout=self.list_timeout)

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

    @_deserialize(CreateArchiveObject)
    def create_archive_object(self, data, extract_archive_param,
                              upload_path='', headers=None,
                              requestslib_kwargs=None):
        """
        Extracts an archive to object(s) via PUT to the storage url
        extract-archive param formats: tar, tar.gz, tar.bz2
        upload_path notes:
        given an archive:

        archive
          file1/name1
          file2/name2
          file3
          file4

        if no upload path is given then the filenames in the archive
        will be extracted to container file1 with obj name1,
        container file2 with obj name2, etc. and obj names without
        slashes will be ignored.

        if the upload path is 'container_foo' all the objects will be
        extracted to 'container_foo' with obj names file1/name1,
        file2/name2, file3...file_n

        if the upload path is container_foo/bar then the objects will
        be extracted to container_foo with the obj name prefix of 'bar'
        ie bar/file1/name1, bar/file2/name2, bar/file3...bar/file_n
        """
        url = '{0}/{1}'.format(
            self.storage_url,
            upload_path)

        params = {"extract-archive": extract_archive_param}

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

    def create_archive(self, object_names, compression_type,
                       archive_name=BULK_ARCHIVE_NAME):
        """
        Bulk creates objects in the opencafe's temp directory specified in the
        engine config. Each object's data will be the md5sum of the object's
        name.

        @type  object_names: strings
        @param object_names: a list of object names

        @type  object_names: string
        @param object_names: file compression to apply to the archive

        @rtype:  string
        @return: Returns full path of the archive that was created in
        opencafe's temp directory specified in the engine config
        """
        supported = [None, "gz", "bz2"]
        if compression_type not in supported:
            raise NameError("supported compression: {0}".format(supported))

        ext = ''

        if not compression_type:
            ext = 'tar'
            compression_type = ''
        else:
            ext = 'tar.{0}'.format(compression_type)

        archive_name = '{0}_{1}.{2}'.format(
            archive_name,
            randstring.get_random_string(),
            ext)

        archive_filename = '{0}/{1}'.format(self.temp_dir, archive_name)
        archive = tarfile.open(
            archive_filename,
            'w:{0}'.format(compression_type))

        for object_name in object_names:
            object_data = get_md5_hash(object_name)
            object_size = len(object_data)
            object_time = int(mktime(datetime.now().timetuple()))

            object_buffer = StringIO(object_data)
            object_buffer.seek(0)

            object_info = tarfile.TarInfo(name=object_name)
            object_info.size = object_size
            object_info.mtime = object_time

            archive.addfile(tarinfo=object_info, fileobj=object_buffer)
        archive.close()

        archive_path = "{0}/{1}".format(
            self.temp_dir,
            archive_name)

        return archive_path
