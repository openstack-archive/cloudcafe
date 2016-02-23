"""
Copyright 2015 Rackspace

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
import datetime
import gzip
import hmac
import json
import uuid

from copy import deepcopy
from hashlib import md5, sha1
from random import choice
from StringIO import StringIO
from time import sleep, time

from cafe.common.unicode import UNICODE_BLOCKS, BLOCK_NAMES
from cafe.engine.behaviors import BaseBehavior, behavior
from cloudcafe.common.tools.md5hash import get_md5_hash
from cloudcafe.objectstorage.objectstorage_api.client \
    import ObjectStorageAPIClient
from cloudcafe.objectstorage.objectstorage_api.config \
    import ObjectStorageAPIConfig


class ObjectStorageAPIBehaviorException(Exception):
    def __init__(self, message, response=None):
        super(ObjectStorageAPIBehaviorException, self).__init__(message)
        self.response = response


class ObjectStorageAPI_Behaviors(BaseBehavior):
    HEADERS_AUTH_TOKEN = 'X-Auth-Token'

    ERROR_INVALID_PATH = 'path must be supplied as a string.'
    ERROR_INVALID_METHOD = 'method must be supplied as a string.'

    def __init__(self, client=None, config=None):
        super(ObjectStorageAPI_Behaviors, self).__init__()
        self.client = client
        if config:
            self.config = config
        else:
            self.config = ObjectStorageAPIConfig()

        self.data_pool = [char for char in UNICODE_BLOCKS.get_range(
            BLOCK_NAMES.basic_latin).encoded_codepoints()]

    def retry_until_success(self, func, func_args=None, func_kwargs=None,
                            success_func=None, max_retries=None,
                            sleep_time=None):
        """
        Allows a function to be re-executed if a success condition is not met.
        The function will be repeatedly executed, with a sleep time between
        retries, until a max retries count is hit. This mechanism ensures that
        eventual consistency does not interfere with test results.

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
        @param max_retries: Perform the function call up until the max
                            number of retries. A default of 5 will be used
                            if no value is passed in.
        @type max_retries: int
        @param sleep_time: The time, in seconds, to sleep between function
                           call retries. A default of 5 seconds will be
                           used if no value is passed in.
        @type sleep_time: int

        @return: The most resent response from calling func.
        @rtype: Response Object
        """
        request_count = 0
        func_args = func_args or []
        func_kwargs = func_kwargs or {}

        def default_success_func(response):
            return response.ok
        success_func = success_func or default_success_func

        # Didn't get a value for max_retries, set to default value from config
        if not max_retries:
            max_retries = self.config.max_retry_count

        # Didn't get a value for sleep_time, set to default value from config
        if not sleep_time:
            sleep_time = self.config.retry_sleep_time

        function_response = None
        while request_count < max_retries:

            # Call function that was passed in with its arguments
            function_response = func(*func_args, **func_kwargs)

            # Check the response with the success function
            if success_func(function_response):
                return function_response

            self._log.info('Retry - HTTP request attempt {} failed '
                           'success_func test.'.format(request_count))

            request_count += 1
            sleep(sleep_time)

        if function_response.ok:
            # If the response came back successful, but the success condition
            # did not occur, then return the response anyway so the caller
            # can deal with how to handle the situation.
            return function_response

        # Log the failure to obtain the success condition
        self._log.debug('Unable to satisfy success condition within {0} '
                        'retries'.format(max_retries))
        # Still going to return the failed response, so the caller can deal
        # with the response appropriately
        return function_response

    def generate_unique_container_name(self, identifier=None):
        """
        Generate a unique container name.

        NOTE: use of this method does not guarantee to create a container
              which is not already in use, but due to the added <random>
              component to the container name, the odds are favorable that
              the container will not already exist.

        @param identifier: can optionally be provided to assist in
                           identification of the purpose of the container
                           when viewing a listing of containers.
        @type identifier: string

        @return: A container name generated in the following format:
                     <base>_<identifier>_<date>_<random>
                 Where:
                     base_container_name - Can be set in the config to
                                           differentiate instances of
                                           CloudCafe.
                     identifier - identifier provided, otherwise this will be
                                  omitted from the container name.
                     date - the date and time that the container name was
                            generated.
                    random - a random string to prevent collisions between
                             test runs.
                 Here are some example generated names:
                    qe_cf_2014-03-08-04-16_040f6242...
                    qe_cf_quick_test_2014-03-08-04-16_040f6242...
        @rtype: string
        """
        parts = []
        parts.append(self.config.base_container_name)
        if identifier:
            parts.append(identifier)
        parts.append(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M'))
        parts.append(str(uuid.uuid4()).replace('-', ''))
        return '_'.join(parts)

    def get_swift_info(self):
        """
        Returns a dictionary of info requested from swift.
        """
        response = self.client.get_swift_info()
        if not response.ok:
            raise Exception('Could not load info from swift.')

        return json.loads(response.content)

    def get_swift_features(self):
        """
        Returns a string representing the enabled features separated by commas.
        """
        info = self.get_swift_info()
        features = ' '.join([k for k in info.viewkeys()])
        return features

    def get_configured_features(self):
        """
        Gets the available features.

        Builds features in the following order:
        1. Get features from swift.
        2. Get features from the config.
        3. Remove any features that are excluded in the config.

        @return: white space separated feature names. or a string constant
                 representing either all or no features are configured.
        @rtype: string
        """
        reported_features = ''
        if self.config.use_swift_info:
            reported_features = self.get_swift_features()

        def split_features(features):
            if features == self.config.ALL_FEATURES:
                return features
            return unicode(features).split()

        # Split the features if needed.
        features = split_features(self.config.features)
        excluded_features = split_features(
            self.config.excluded_features)

        if features == self.config.ALL_FEATURES:
            return features

        reported_features = reported_features.split()
        features = list(set(reported_features) | set(features))

        # If all features are to be ignored, skip
        if excluded_features == self.config.ALL_FEATURES:
            return self.config.NO_FEATURES

        # Remove all features
        for feature in excluded_features:
            try:
                index = features.index(feature)
                features.pop(index)
            except ValueError:
                pass

        return ' '.join(features)

    def container_exists(self, name=None):
        path = '/{0}'.format(name)
        response = self.request('HEAD', path)

        if response.status_code == 404:
            return False

        if not response.ok:
            raise Exception(
                'Error checking the existence of container "{0}"'.format(
                    str(name)))

        return True

    def create_container(self, container_name, log_delivery=False,
                         headers=None):

        if log_delivery:
            headers['X-Container-Meta-Access-Log-Delivery'] = str(True)

        response = self.client.create_container(
            container_name,
            headers=headers)

        if not response.ok:
            raise Exception(
                'could not create container "{0}"'.format(str(container_name)))

    def list_containers(self, headers=None, params=None,
                        expected_containers=None, requestslib_kwargs=None):
        """
        List containers in a account.  This method allows for a success
        function to be provided, ensuring that the system has stabilized and
        become consistent.

        @param headers: headers to be added to the HTTP request.
        @type  headers: dictionary
        @param params: query string parameters to be added to the HTTP request.
        @type  params: dictionary
        @param expected_containers: container names expected to be in the
                                    account listing.
        @type  expected_containers: list
        @param requestslib_kwargs: keyword arguments to be passed on to
                                   python requests.
        @type  requestslib_kwargs: dictionary

        @return: container listing
        @rtype: list
        """
        if not expected_containers:
            expected_containers = []

        def success_func(response):
            if not response.ok:
                return False
            for name in expected_containers:
                if name not in response.content:
                    return False
            return True

        response = self.retry_until_success(
            self.client.list_containers,
            func_kwargs={
                'headers': headers,
                'params': params,
                'requestslib_kwargs': requestslib_kwargs},
            success_func=success_func,
            max_retries=10)
        return response.entity

    def create_object(self, container_name, object_name, data=None,
                      headers=None, params=None):
        if not self.container_exists(container_name):
            self.create_container(container_name)
        if not headers:
            headers = {}

        if data and 'content-length' not in headers:
            headers['content-length'] = str(len(data))

        response = self.client.create_object(
            container_name,
            object_name,
            data=data,
            headers=headers,
            params=params)

        if not response.ok:
            raise Exception('could not create object "{0}/{1}"'.format(
                container_name, object_name))

    def create_static_large_object(self, container_name, object_name,
                                   segments_info=None, manifest=None,
                                   headers=None):
        """
        Create a Static Large Object via one of two methods. If a list of
        segments is received, use that info to create all the segment
        objects, generate the manifest, and upload the manifest. If a
        manifest file is received, assume that the objects have already been
        created and simply upload the manifest file.

        @param container_name: Name of container to upload manifest
        @type container_name: string
        @param object_name: Name of SLO object
        @type object_name: string
        @param segments_info: A list of segment objects that will be
                              created. Each segment object should have the
                              following data:
            container_name - the container where the segment will be created
            segment_name - the name of the segment
            segment_size - The size of the segment. Note that the min
            segment size for SLOs is 1MB, except for the final segment.
        @type segments_info: List of dictionaries
        @param manifest: An ordered list of files in JSON data format. The
                         data to be supplied for each segment is as follows:
            path - The container and object name in the following format:
            containerName/objectName
            etag - The ETag header from the successful 201 response of the PUT
            operation that uploaded the segment. This is the MD5 checksum of
            the segment object's data.
            size_bytes - The segment object's size in bytes. This value must
            match the Content-Length of that object.
        @type manifest: List of dictionaries
        @param headers: Headers to be added to HTTP request
        @type headers: dictionary
        @param params: Query string parameters to be added to the request
        @type params: dictionary

        @return: Response for manifest upload
        @rtype: Response Object
        """

        # If segment info was received, create the segments, then create
        # the manifest, and finally upload the manifest.
        if segments_info and not manifest:
            slo_manifest = []

            for segment in segments_info:

                if "container_name" not in segment:
                    raise ObjectStorageAPIBehaviorException(
                        "Can't create a segment without a container")
                if "segment_name" not in segment:
                    raise ObjectStorageAPIBehaviorException(
                        "Can't create a segment without a name")
                if "segment_size" not in segment:
                    raise ObjectStorageAPIBehaviorException(
                        "Can't create a segment without a size")

                segment_data = ''.join([choice(self.data_pool) for x in xrange(
                    segment.get("segment_size"))])
                segment_etag = md5(segment_data).hexdigest()

                segment_response = self.client.create_object(
                    container_name,
                    segment.get("segment_name"),
                    data=segment_data)

                if not segment_response.ok:
                    raise Exception(
                        "Failed to create SLO Segment {0}/{1}".format(
                            container_name, segment.get("segment_name")))

                slo_manifest.append({
                    'path': '/{0}/{1}'.format(
                        container_name, segment.get("segment_name")),
                    'etag': segment_etag,
                    'size_bytes': len(segment_data)})

            manifest_response = self.client.create_object(
                container_name,
                object_name,
                data=json.dumps(slo_manifest),
                params={'multipart-manifest': 'put'}, headers=headers)

            return manifest_response

        # If a manifest is received assume that the segment objects exist
        # and upload the manifest file.
        if manifest and not segments_info:
            manifest_response = self.client.create_object(
                container_name,
                object_name,
                data=json.dumps(manifest),
                params={'multipart-manifest': 'put'}, headers=headers)

            return manifest_response

    def decompress_object(self, container_name, object_name,
                          headers=None, params=None, stream=False,
                          requestslib_kwargs=None):
        """
        decompresses the content of an object.

        @param container_name: container name
        @type  container_name: string
        @param obj_name: object name
        @type  obj_name: string
        @param headers: headers to be added to the HTTP request.
        @type  headers: dictionary
        @param params: query string parameters to be added to the HTTP request.
        @type  params: dictionary
        @param requestslib_kwargs: keyword arguments to be passed on to
                                   python requests.
        @type  requestslib_kwargs: dictionary

        @return: decompressed content
        @rtype: list
        """

        response = self.client.get_object(
            container_name,
            object_name,
            headers=headers,
            params=params,
            requestslib_kwargs={'stream': stream})

        opened_file = gzip.GzipFile(
            mode='rb',
            fileobj=StringIO(response.content))
        uncompressed_data = opened_file.readlines()
        opened_file.close()

        return uncompressed_data

    def request(self, method=None, path='', **kwargs):
        """
        Make a HTTP request against the client's acccount.  This request
        should make no assumptions and do no setup for you.  It shuold be
        considered a dumb request that does exactly what you tell it.

        @type  method: string
        @param method: the value to use as the HTTP method.
        @type  path: string
        @param path: the value representing the path to the container/object
            you would like to make the request against.  If you want to
            make a request against the account, the path field can be omitted.

        @rtype:  object(requests.Response)
        @return: a Requests Libray response object.
        """
        if type(path) is not str:
            raise TypeError(self.ERROR_INVALID_METHOD)

        url = '{0}{1}'.format(self.client.storage_url, path)
        response = self.client.request(
            method, url, requestslib_kwargs=kwargs)

        return response

    def get_object_count(self, container_name, headers=None, params=None,
                         expected_object_count=None, requestslib_kwargs=None):
        """
        Get the number of objects in a container.  This method allows for a
        success function to be provided, ensuring that the system has
        stabilized and become consistent.

        @param container_name: container to list the object from.
        @type  container_name: string
        @param headers: headers to be added to the HTTP request.
        @type  headers: dictionary
        @param params: query string parameters to be added to the HTTP request.
        @type  params: dictionary
        @param expected_object_count: object names expected to be in the
                                      container listing.
        @type  expected_object_count: int
        @param requestslib_kwargs: keyword arguments to be passed on to
                                   python requests.
        @type  requestslib_kwargs: dictionary

        @return: object listing
        @rtype: int
        """

        def success_func(response):
            object_count = response.headers.get('x-container-object-count')
            if not response.ok or object_count is None:
                return False
            if expected_object_count != object_count:
                return False
            return True

        response = self.retry_until_success(
            self.client.get_container_metadata,
            func_args=[container_name],
            func_kwargs={'requestslib_kwargs': requestslib_kwargs},
            success_func=success_func,
            max_retries=10)

        return int(response.headers.get('x-container-object-count'))

    def list_objects(self, container_name, headers=None, params=None,
                     expected_objects=None, requestslib_kwargs=None):
        """
        List objects in a container.  This method allows for a success
        function to be provided, ensuring that the system has stabilized and
        become consistent.

        @param container_name: container to list the object from.
        @type  container_name: string
        @param headers: headers to be added to the HTTP request.
        @type  headers: dictionary
        @param params: query string parameters to be added to the HTTP request.
        @type  params: dictionary
        @param expected_objects: object names expected to be in the container
                                 listing.
        @type  expected_objects: list
        @param requestslib_kwargs: keyword arguments to be passed on to
                                   python requests.
        @type  requestslib_kwargs: dictionary

        @return: object listing
        @rtype: list
        """
        if not expected_objects:
            expected_objects = []

        def success_func(response):
            if not response.ok:
                return False
            for name in expected_objects:
                if name not in response.content:
                    return False
            return True

        response = self.retry_until_success(
            self.client.list_objects,
            func_args=[container_name],
            func_kwargs={
                'headers': headers,
                'params': params,
                'requestslib_kwargs': requestslib_kwargs},
            success_func=success_func,
            max_retries=10)
        return response.entity

    def authed_request(self, method=None, path='', **kwargs):
        """
        Same as request, except the auth token is automatically added to
        the headers for the request.

        @type  method: string
        @param method: the value to use as the HTTP method.
        @type  path: string
        @param path: the value representing the path to the container/object
            you would like to make the request against.  If you want to
            make a request against the account, the path field can be omitted.

        @rtype:  object(requests.Response)
        @return: a Requests Libray response object.
        """
        new_args = [method, path]
        new_kwargs = deepcopy(kwargs)

        if 'headers' not in new_kwargs:
            new_kwargs['headers'] = \
                {self.HEADERS_AUTH_TOKEN: self.client.auth_token}
        else:
            auth_provided = bool(
                [x for x in new_kwargs['headers'] if
                    x.lower() == self.HEADERS_AUTH_TOKEN.lower()])
            if not auth_provided:
                new_kwargs['headers'][self.HEADERS_AUTH_TOKEN] = \
                    self.auth_token

        response = self.request(*new_args, **new_kwargs)

        return response

    def get_tempurl_key(self):
        """
        @summary: Check to see if the account currently has tempurl keys set
        and return the first tempurl key if so. Otherwise, attempt to set the
        keys to a default state and return the first tempurl key.

        @return Account tempurl key
        @rtype String
        """
        acct_temp_keys_set = self.check_account_tempurl_keys()
        if acct_temp_keys_set:
            metadata_response = self.client.get_account_metadata()
        else:
            self.set_default_account_tempurl_keys()
            metadata_response = self.client.get_account_metadata()

        return metadata_response.headers.get("X-Account-Meta-Temp-Url-Key")

    @behavior(ObjectStorageAPIClient)
    def check_account_tempurl_keys(self):
        """
        Check the current account tempurl keys to ensure that they exist.
        If they don't exist, call set_default_account_tempurl_keys() to set
        the account keys to default values. Then recursively check the keys
        again to make sure they are properly set.

        @return: True/False
        @rtype:  Boolean
        """
        metadata_response = self.client.get_account_metadata()

        current_key_one = metadata_response.headers.get(
            'x-account-meta-temp-url-key')
        current_key_two = metadata_response.headers.get(
            'x-account-meta-temp-url-key-2')

        if current_key_one and current_key_two:
            return True
        else:
            self.set_default_account_tempurl_keys()

            metadata_response = self.client.get_account_metadata()
            if not metadata_response.headers.get(
                    'X-Account-Meta-Temp-URL-Key'):
                return False
            if not metadata_response.headers.get(
                    'X-Account-Meta-Temp-URL-Key-2'):
                return False

    def set_default_account_tempurl_keys(self):
        """
        Set the account tempurl keys to default values based on the constant
        VALID_TEMPURL_KEY. This function will throw exceptions if either key
        fails to be set.
        """
        # Set tempurl key one to default value
        key_one = '{0}_one'.format(self.VALID_TEMPURL_KEY)
        key_one_headers = {'X-Account-Meta-Temp-URL-Key': key_one}
        key_one_response = self.client.set_temp_url_key(
            headers=key_one_headers)

        if not key_one_response.ok:
            raise Exception('Could not set TempURL key one.')

        # Set tempurl key two to default value
        key_two = '{0}_two'.format(self.VALID_TEMPURL_KEY)
        key_two_headers = {'X-Account-Meta-Temp-URL-Key-2': key_two}
        key_two_response = self.client.set_temp_url_key(
            headers=key_two_headers)

        if not key_two_response.ok:
            raise Exception('Could not set TempURL key two.')

    def _purge_container(self, container_name, max_recursion, call_count=1,
                         requestslib_kwargs=None):
        """
        @summary: List all the objects in a container and then attempt to
        delete them all. List the objects again and recursively call
        _purge_container if the container listing returns a 200 (indicating
        that there are still objects left).

        @param container_name: name of a container
        @type container_name: string
        @param max_recursion:  the maximum number of times for this method
                               to recursively call itself.
        @type max_recursion:   int
        @param call_count: the number of iterations that have been recursively
                           called, defaults to 1.
        @type call_count:  int
        """

        params = {'format': 'json'}
        list_response = self.client.list_objects(
            container_name,
            params=params,
            requestslib_kwargs=requestslib_kwargs)

        for storage_object in list_response.entity:
            self.client.delete_object(container_name, storage_object.name)

        list_response = self.client.list_objects(container_name)

        # If the list response returns objects, purge again
        if list_response.status_code == 200:
            if call_count > max_recursion:
                self._log_cleanup_failure(container_name)
                raise Exception('Failed to purge objects from {0} '
                                'after {1} tries.'.format(container_name,
                                                          call_count))
            else:
                self._purge_container(container_name,
                                      max_recursion=max_recursion,
                                      call_count=call_count + 1,
                                      requestslib_kwargs=requestslib_kwargs)

    def force_delete_container(self, container_name,
                               requestslib_kwargs=None):
        """
        @summary: Calls purge container to delete all the objects in a
        container. Then it will attempt to delete the container with a retry
        until success function. This will handle cases where object deletion
        is slow and caused conflicts.

        @param container_name: Name of container to purge and delete
        @type container_name: string
        """

        def success_func(response):
            return response.status_code == 204 or response.status_code == 404

        self._purge_container(container_name,
                              max_recursion=30,
                              requestslib_kwargs=requestslib_kwargs)

        delete_response = self.retry_until_success(
            self.client.delete_container,
            func_args=[container_name],
            func_kwargs={'requestslib_kwargs': requestslib_kwargs},
            success_func=success_func,
            max_retries=self.config.max_retry_count,
            sleep_time=self.config.retry_sleep_time)

        if delete_response.status_code == 409:
            self._log.debug("force delete failure {0} status {1}".format(
                container_name,
                delete_response.status_code))
            self._log_cleanup_failure(container_name)

    def force_delete_containers(self, container_list,
                                requestslib_kwargs=None):
        """
        @summary: Calls force_delete_container on a list of containers

        @param container_list: a list of containers
        @type container_list: list
        """
        for container_name in container_list:
            self.force_delete_container(
                container_name, requestslib_kwargs=requestslib_kwargs)

    def create_formpost(self, container, files, object_prefix='',
                        redirect='http://example.com/formpost',
                        max_file_size=104857600, max_file_count=10,
                        expires=None, key='', signature="",
                        x_delete_at=None, x_delete_after=None):
        """
        Creates a multipart/form-data body (RFC-2388) that can be used for
        POSTs to Swift.

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
        @param signature: The HMAC-SHA1 signature of the form.
        @type signature: string
        @param x_delete_at: The unix time relating to when the object will
                            be deleted from the container.
        @type x_delete_at: int
        @param x_delete_after: The amount of time, in seconds, after which
                               the object will be deleted from the container.
        @type x_delete_after: int

        @return: Data to be POSTed in the following format:
            {
                'target_url': '<url to POST to>',
                'headers': '<headers to be added to the request>,
                'body': '<body to be posted to the target url>'
            }
        @rtype: dictionary
        """
        base_url, account_hash = self.client.storage_url.split('/v1/')
        path = '/v1/{0}/{1}'.format(account_hash, container)
        if object_prefix:
            path = '{0}/{1}'.format(path, object_prefix)

        if not expires:
            expires = int(time() + 600)

        url = ''.join([base_url, path])
        hmac_body = '{0}\n{1}\n{2}\n{3}\n{4}'.format(
            path, redirect, max_file_size, max_file_count, expires)
        if not signature:
            signature = hmac.new(key, hmac_body, sha1).hexdigest()

        form = []
        if redirect:
            form.append({
                'headers':
                {'Content-Disposition': 'form-data; name="redirect"'},
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
        if x_delete_at:
            form.append({
                'headers': {'Content-Disposition':
                            'form-data; name="x_delete_at"'},
                'data': str(x_delete_at)})
        if x_delete_after:
            form.append({
                'headers': {'Content-Disposition':
                            'form-data; name="x_delete_after"'},
                'data': str(x_delete_after)})
        form.append({
            'headers': {'Content-Disposition': 'form-data; name="signature"'},
            'data': signature})

        for data_file in files:
            form_name = data_file.get('name')
            form_filename = data_file.get('filename', form_name)
            form_content_type = data_file.get('content_type', 'text/plain')
            form_data = data_file.get('data', get_md5_hash(form_name))
            form.append({
                'headers': {'Content-Disposition':
                            'form-data; name="{0}"; filename="{1}"'.format(
                                form_name, form_filename),
                        'Content-Type': form_content_type},
                'data': form_data})

        data = []
        boundary = '----WebKitFormBoundary40Q4WaJHO84PBBIa'

        for section in form:
            data.append('--{0}\r\n'.format(boundary))
            for key, value in section['headers'].iteritems():
                data.append('{0}: {1}\r\n'.format(key, value))
            data.append('\r\n')
            data.append(section['data'])
            data.append('\r\n')
        data.append('\r\n--{0}'.format(boundary))

        post_headers = {
            'Cache-Control': 'max-age=0',
            'Accept': '*/*;q=0.8',
            'Content-Type': 'multipart/form-data; boundary={0}'.format(
                boundary)}

        return {'target_url': url, 'headers': post_headers,
                'body': ''.join(data)}

    def _log_cleanup_failure(self, container_name):
        """
        @summary: This method will create a failure object in a failure
        container, so that it can be cleaned up separately. The failure
        object's data will be the container that failed to clean up properly
        during testing.

        @param container_name: Name of container that failed to clean up.
        @type container_name: string
        """
        # Create a unique failure log name
        failure_log_name = "cleanup_failure_{0}_{1}".format(
            datetime.datetime.now().strftime('%Y-%m-%d-%H-%M'),
            str(uuid.uuid4()).replace('-', ''))

        # Create an object in the failure container with the data being the
        # container that was not cleaned up properly
        self.create_object(
            container_name=self.config.cleanup_failure_container_name,
            object_name=failure_log_name,
            data=container_name)
