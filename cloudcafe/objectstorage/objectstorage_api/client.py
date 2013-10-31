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
import tarfile

from cloudcafe.common.tools import randomstring as randstring
from cafe.engine.config import EngineConfig
from cStringIO import StringIO
from time import time, mktime
from hashlib import sha1
from datetime import datetime
from cloudcafe.common.tools.md5hash import get_md5_hash
from cafe.engine.clients.rest import RestClient

BULK_ARCHIVE_NAME = 'bulk_objects'


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

    def list_containers(self, headers={}, params={}):
        """
        Lists all containers for the account.

        If the 'format' variable is passed as part of the 'params'
        dictionary, an object representing the deserialized version of
        that format (either xml or json) will be appended to the response
        as the 'entity' attribute. (ie, response.entity)
        """
        response = self.get(self.storage_url, headers=headers, params=params)

        return response

    #Container-----------------------------------------------------------------

    def get_container_metadata(self, container_name, headers={}):
        url = '{0}/{1}'.format(self.storage_url, container_name)

        response = self.head(url, headers=headers)

        return response

    def create_container(self, container_name, headers={}):
        url = '{0}/{1}'.format(self.storage_url, container_name)

        response = self.put(url, headers=headers)

        return response

    def delete_container(self, container_name, headers={}):
        url = '{0}/{1}'.format(self.storage_url, container_name)

        response = self.delete(url, headers=headers)

        return response

    def set_container_metadata(self, container_name, headers={}):
        url = '{0}/{1}'.format(self.storage_url, container_name)

        response = self.post(url, headers=headers)

        return response

    def get_container_options(self, container_name, headers={}):
        """
        returns response from CORS option call
        """
        url = '{0}/{1}'.format(self.storage_url, container_name)

        response = self.options(url, headers=headers)

        return response

    def list_objects(self, container_name, headers={}, params={}):
        """
        Lists all objects in the specified container.

        If the 'format' variable is passed as part of the 'params'
        dictionary, an object representing the deserialized version of
        that format (either xml or json) will be appended to the response
        as the 'entity' attribute. (ie, response.entity)
        """
        url = '{0}/{1}'.format(self.storage_url, container_name)

        response = self.get(url, headers=headers, params=params)

        return response

    def get_object_count(self, container_name):
        """
        Returns the number of objects in a container.
        """
        response = self.get_container_metadata(container_name)

        obj_count = int(response.headers.get('x-container-object-count'))

        return obj_count

    def _purge_container(self, container_name):
        params = {'format': 'json'}
        response = self.list_objects(container_name, params=params)
        try:
            json_data = json.loads(response.content)
            for entry in json_data:
                self.delete_object(container_name, entry['name'])
        except ValueError:
            pass

        return self.delete_container(container_name)

    def force_delete_containers(self, container_list):
        for container_name in container_list:
            return self._purge_container(container_name)

    #Storage Object------------------------------------------------------------

    def get_object(self, container_name, object_name, headers={}, params={},
                   stream=False):
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

    def create_object(self, container_name, object_name, data=None, headers={},
                      params={}):
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

        response = self.put(url, data=data, headers=headers, params=params)

        return response

    def copy_object(self, container_name, object_name, headers={}):
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

        response = self.request(method=method, url=url, headers=headers)

        return response

    def delete_object(self, container_name, object_name, headers={}):
        url = '{0}/{1}/{2}'.format(
            self.storage_url,
            container_name,
            object_name)

        response = self.delete(url, headers=headers)

        return response

    def get_object_metadata(self, container_name, object_name, headers={}):
        url = '{0}/{1}/{2}'.format(
            self.storage_url,
            container_name,
            object_name)

        response = self.head(url, headers=headers)

        return response

    def set_object_metadata(self, container_name, object_name, headers={}):
        url = '{0}/{1}/{2}'.format(
            self.storage_url,
            container_name,
            object_name)

        response = self.post(url, headers=headers)

        return response

    def set_temp_url_key(self, headers={}):
        response = self.post(self.storage_url, headers=headers)

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

        archive_name = '{0}.{1}.{2}'.format(
            archive_name,
            randstring.get_random_string(),
            ext)

        archive_dir = self.engine_config.temp_directory
        archive_filename = '{0}/{1}'.format(archive_dir, archive_name)
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
            self.engine_config.temp_directory,
            archive_name)

        return archive_path
