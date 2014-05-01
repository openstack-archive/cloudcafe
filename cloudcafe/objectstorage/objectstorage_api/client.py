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
import requests
import tarfile
import urllib
from cStringIO import StringIO
from datetime import datetime
from hashlib import sha1
from os.path import expanduser
from time import time, mktime

from cafe.common.reporting import cclogging
from cafe.engine.config import EngineConfig
from cafe.engine.http.client import HTTPClient
from cloudcafe.common.tools import randomstring as randstring
from cloudcafe.common.tools.md5hash import get_md5_hash
from cloudcafe.objectstorage.objectstorage_api.models.responses \
    import AccountContainersList, ContainerObjectsList, CreateArchiveObject
from cloudcafe.objectstorage.objectstorage_api.deserialization_decorator \
    import deserialize

BULK_ARCHIVE_NAME = 'bulk_objects'


def _log_transaction(log, level=cclogging.logging.DEBUG):
    """
    This is a copy from cafe.engine.http_client._log_transaction, this was
    necessary to reduce the size of the logs for object storage tests.
    The only differences are that the logged bodies of the requests/response
    have been truncated if over 100 bytes (this has been noted below for
    reference)

    Paramaterized decorator
    Takes a python Logger object and an optional logging level.
    """
    def _decorator(func):
        """Accepts a function and returns wrapped version of that function."""
        def _wrapper(*args, **kwargs):
            """Logging wrapper for any method that returns a requests response.
            Logs requestslib response objects, and the args and kwargs
            sent to the request() method, to the provided log at the provided
            log level.
            """
            logline = '{0} {1}'.format(args, kwargs)

            try:
                log.debug(logline.decode('utf-8', 'replace'))
            except Exception as exception:
                #Ignore all exceptions that happen in logging, then log them
                log.info(
                    'Exception occured while logging signature of calling'
                    'method in http client')
                log.exception(exception)

            #Make the request and time it's execution
            response = None
            elapsed = None
            try:
                start = time()
                response = func(*args, **kwargs)
                elapsed = time() - start
            except Exception as exception:
                log.critical('Call to Requests failed due to exception')
                log.exception(exception)
                raise exception

            #requests lib 1.0.0 renamed body to data in the request object
            request_body = ''
            if 'body' in dir(response.request):
                request_body = response.request.body
            elif 'data' in dir(response.request):
                request_body = response.request.data
            else:
                log.info(
                    "Unable to log request body, neither a 'data' nor a "
                    "'body' object could be found")

            # NOTE: Truncating request_body if > 100 bytes.
            if request_body and len(request_body) > 100:
                request_body = '{0}...<truncated>'.format(request_body[:100])

            #requests lib 1.0.4 removed params from response.request
            request_params = ''
            request_url = response.request.url
            if 'params' in dir(response.request):
                request_params = response.request.params
            elif '?' in request_url:
                request_url, request_params = request_url.split('?')

            logline = ''.join([
                '\n{0}\nREQUEST SENT\n{0}\n'.format('-' * 12),
                'request method..: {0}\n'.format(response.request.method),
                'request url.....: {0}\n'.format(request_url),
                'request params..: {0}\n'.format(request_params),
                'request headers.: {0}\n'.format(response.request.headers),
                'request body....: {0}\n'.format(request_body)])
            try:
                log.log(level, logline.decode('utf-8', 'replace'))
            except Exception as exception:
                #Ignore all exceptions that happen in logging, then log them
                log.log(level, '\n{0}\nREQUEST INFO\n{0}\n'.format('-' * 12))
                log.exception(exception)

            # NOTE: Truncating request_body if > 100 bytes.
            response_content = response.content
            if response_content and len(response_content) > 100:
                response_content = '{0}...<truncated>'.format(
                    response_content[:100])

            logline = ''.join([
                '\n{0}\nRESPONSE RECEIVED\n{0}\n'.format('-' * 17),
                'response status..: {0}\n'.format(response),
                'response time....: {0}\n'.format(elapsed),
                'response headers.: {0}\n'.format(response.headers),
                'response body....: {0}\n'.format(response_content),
                '-' * 79])
            try:
                log.log(level, logline.decode('utf-8', 'replace'))
            except Exception as exception:
                #Ignore all exceptions that happen in logging, then log them
                log.log(level, '\n{0}\nRESPONSE INFO\n{0}\n'.format('-' * 13))
                log.exception(exception)
            return response
        return _wrapper
    return _decorator


class ObjectStorageAPIClient(HTTPClient):
    _log = cclogging.getLogger(__name__)

    def __init__(self, storage_url, auth_token, base_container_name=None,
                 base_object_name=None):
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

    @_log_transaction(log=_log)
    def request(
            self, method, url, headers=None, params=None, data=None,
            requestslib_kwargs=None):
        """
        Overrides the HTTPClient's 'request' method, to prevent it from calling
        BaseHTTPClient's 'request' method, so we can provide our
        own logging decorator.

        @param method: HTTP method to use in the request.
        @type method: string
        @param url: URL to make the request to.
        @type url: string
        @param: headers: headers to use with the request.
        @type headers: dict
        @param: params: query string parameters to use with the request.
        @type param: dict
        @param data: data to send in the reqest.
        @type data: string
        @param requestlib_kwargs: kwargs to be passed to requests.
        @type requestlib_kwargs: dict
        """
        #set requestslib_kwargs to an empty dict if None
        requestslib_kwargs = requestslib_kwargs if (
            requestslib_kwargs is not None) else {}

        #Set defaults
        params = params if params is not None else {}
        verify = False

        #If headers are provided by both, headers "wins" over default_headers
        headers = dict(self.default_headers, **(headers or {}))

        #Override url if present in requestslib_kwargs
        if 'url' in requestslib_kwargs.keys():
            url = requestslib_kwargs.get('url', None) or url
            del requestslib_kwargs['url']

        #Override method if present in requestslib_kwargs
        if 'method' in requestslib_kwargs.keys():
            method = requestslib_kwargs.get('method', None) or method
            del requestslib_kwargs['method']

        #The requests lib already removes None key/value pairs, but we force it
        #here in case that behavior ever changes
        for key in requestslib_kwargs.keys():
            if requestslib_kwargs[key] is None:
                del requestslib_kwargs[key]

        #Create the final parameters for the call to the base request()
        #Wherever a parameter is provided both by the calling method AND
        #the requests_lib kwargs dictionary, requestslib_kwargs "wins"
        requestslib_kwargs = dict({'headers': headers,
                                   'params': params,
                                   'verify': verify,
                                   'data': data},
                                  **requestslib_kwargs)

        #Make the request
        return requests.request(method, url, **requestslib_kwargs)

    def get_swift_info(self, headers=None, params=None,
                       requestslib_kwargs=None):
        """
        Returns Swift info.

        @param headers: headers to be added to the HTTP request.
        @type  headers: dictionary
        @param params: query string parameters to be added to the HTTP request.
        @type  params: dictionary
        @param requestslib_kwargs: keyword arguments to be passed on to
                                   python requests.
        @type requestslib_kwargs: dictionary

        @return: Swift info
        @rtype: response object
        """
        info_url = '{0}/info'.format(self.swift_endpoint)
        return self.get(info_url,
                        headers=headers,
                        params=params,
                        requestslib_kwargs=requestslib_kwargs)

    #Account-------------------------------------------------------------------

    def retrieve_account_metadata(self):
        response = self.head(self.storage_url)

        return response

    @deserialize(AccountContainersList)
    def list_containers(self, headers=None, params=None,
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

    @deserialize(ContainerObjectsList)
    def list_objects(self, container_name, headers=None, params=None,
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

    @deserialize(CreateArchiveObject)
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

    def create_formpost(self, container, files, object_prefix='',
                        redirect='http://example.com/formpost',
                        max_file_size=104857600, max_file_count=10,
                        expires=None, key=''):
        """
        Creates RFC-2388.

        @param container: Name of the container to post objects to.
        @type  container: string
        @param files: Files to post in the form.  The dictionaries representing
                      a file should be formatted as follows:
                      {
                          'name': '<form name>',
                          'filename': '<filename>',
                          'content_type': '<content_type>',
                          'data': '<filedata>'
                      }
                      Where only name is required, defaults to other values
                      will be as follows:
                          filename - the value stored in name.
                          content_type - 'text/plain'
                          data - the md5 hash of the value stored in name.
        @type  files: list of dictionaries
        @param object_prefix: prefix to be used in the name of the objects
                              created.
        @type  object_prefix: string
        @param redirect: URL to be returned as the 'location' header in the
                         HTTP response.
        @type  redirect: string
        @param max_file_size: The maximum file size in bytes which can be
                              uploaded with the form.
        @type  max_file_size: int
        @param max_file_count: The maximum number of files allowed to be
                               uploaded with the form.
        @type  max_file_count: int
        @param expires: The unix time relating to when the form expires
                        and will no longer allow uploads to the container.
        @type  expires: int
        @param key: The account's X-Tempurl-Key used in creating the signatre
                    which authorizes the form to be POSTed.
        @type  key: string

        @return: Data to be POSTed in the following format:
            {
                'target_url': '<url to POST to>',
                'headers': '<headers to be added to the request>,
                'body': '<body to be posted to the target url>'
            }
        @rtype: dictionary
        """
        base_url, path = self.storage_url.split('/v1')
        path = '/v1{0}/{1}'.format(path, container)
        if object_prefix:
            path = '{0}/{1}'.format(path, object_prefix)

        if not expires:
            expires = int(time() + 600)

        url = ''.join([base_url, path])
        hmac_body = '{0}\n{1}\n{2}\n{3}\n{4}'.format(
            path, redirect, max_file_size, max_file_count, expires)
        sig = hmac.new(key, hmac_body, sha1).hexdigest()

        form = []
        form.append({
            'headers': {'Content-Disposition': 'form-data; name="redirect"'},
            'data': redirect})
        form.append({
            'headers': {'Content-Disposition':
                        'form-data; name="max_file_size"'},
            'data': str(max_file_size)})
        form.append({
            'headers': {'Content-Disposition':
                        'form-data; name="max_file_count"'},
            'data': str(max_file_count)})
        form.append({
            'headers': {'Content-Disposition': 'form-data; name="expires"'},
            'data': str(expires)})
        form.append({
            'headers': {'Content-Disposition': 'form-data; name="signature"'},
            'data': sig})
        for f in files:
            form_name = f.get('name')
            form_filename = f.get('filename', form_name)
            form_content_type = f.get('content_type', 'text/plain')
            form_data = f.get('data', get_md5_hash(form_name))
            form.append({
                'headers': {'Content-Disposition':
                            'form-data; name="{0}"; filename="{1}"'.format(
                                form_name, form_filename),
                        'Content-Type': form_content_type},
                'data': form_data})

        data = []
        boundry = '----WebKitFormBoundary40Q4WaJHO84PBBIa'

        for section in form:
            data.append('--{0}\r\n'.format(boundry))
            for key, value in section['headers'].iteritems():
                data.append('{0}: {1}\r\n'.format(key, value))
            data.append('\r\n')
            data.append(section['data'])
            data.append('\r\n')
        data.append('\r\n--{0}'.format(boundry))

        post_headers = {
            'Cache-Control': 'max-age=0',
            'Accept': '*/*;q=0.8',
            'Content-Type': 'multipart/form-data; boundary={0}'.format(
                boundry)}

        return {'target_url': url, 'headers': post_headers,
                'body': ''.join(data)}

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

    def bulk_delete(self, targets, headers=None, requestslib_kwargs=None):
        """
        Deletes container/objects from an account.

        @type  targets: list of strings
        @param targets: A list of the '/container/object' or '/container'
            to be bulk deleted.  Note, bulk delete will not remove
            containers that have objects in them, and there is limit of
            1000 containers/objects per delete.

        @rtype:  object
        @return: The requests response object returned from the call.
        """
        if not headers:
            headers = {}
        url = '{0}{1}'.format(self.storage_url, '?bulk-delete')
        data = '\n'.join([urllib.quote(target) for target in targets])
        headers['content-type'] = 'text/plain'
        headers['content-length'] = str(len(data))

        response = self.request(
            'DELETE', url, data=data, headers=headers,
            requestslib_kwargs=requestslib_kwargs)

        return response
