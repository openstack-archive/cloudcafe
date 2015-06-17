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
import uuid
import json
import gzip
from StringIO import StringIO
from copy import deepcopy
from time import sleep
from random import choice
from hashlib import md5
from cafe.engine.behaviors import BaseBehavior, behavior
from cloudcafe.objectstorage.objectstorage_api.config \
    import ObjectStorageAPIConfig
from cloudcafe.objectstorage.objectstorage_api.client \
    import ObjectStorageAPIClient
from cafe.common.unicode import UNICODE_BLOCKS, BLOCK_NAMES


class ObjectStorageAPIBehaviorException(Exception):
    def __init__(self, message, response=None):
        super(ObjectStorageAPIBehaviorException, self).__init__(message)
        self.response = response


class ObjectStorageAPI_Behaviors(BaseBehavior):
    HEADERS_AUTH_TOKEN = 'X-Auth-Token'

    PATH_TYPES_ACCOUNT = 'account'
    PATH_TYPES_CONTAINER = 'container'
    PATH_TYPES_OBJECT = 'object'

    ERROR_INVALID_PATH = 'path must be supplied as a string.'
    ERROR_INVALID_METHOD = 'method must be supplied as a string.'

    VALID_OBJECT_NAME = 'object'
    VALID_OBJECT_NAME_WITH_SLASH = 'object/foo'
    VALID_OBJECT_NAME_WITH_TRAILING_SLASH = 'object/'
    VALID_OBJECT_NAME_WITH_UNICODE = 'object<insert_unicode_here>foo'
    VALID_OBJECT_DATA = 'object data.'

    VALID_TEMPURL_KEY = 'qe-tempurl-key'

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
        raise ObjectStorageAPIBehaviorException(
            'Unable to satisfy success condition within {0} retries'.format(
                max_retries), function_response)

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

    @behavior(ObjectStorageAPIClient)
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

    @behavior(ObjectStorageAPIClient)
    def container_exists(self, name=None):
        path = '/{0}'.format(name)
        response = self.request('HEAD', path)

        if response.status_code == 404:
            return False

        if not response.ok:
            raise Exception(
                'Error checking the existance of container  "{0}"'.format(
                    str(name)))

        return True

    @behavior(ObjectStorageAPIClient)
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

    @behavior(ObjectStorageAPIClient)
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

    @behavior(ObjectStorageAPIClient)
    def create_object(self, container_name, object_name, data=None,
                      headers=None, params=None):
        if not self.container_exists(container_name):
            self.create_container(container_name)

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

    @behavior(ObjectStorageAPIClient)
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

    @behavior(ObjectStorageAPIClient)
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

    @behavior(ObjectStorageAPIClient)
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

    @behavior(ObjectStorageAPIClient)
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

    @behavior(ObjectStorageAPIClient)
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

    @behavior(ObjectStorageAPIClient)
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

    @behavior(ObjectStorageAPIClient)
    def get_tempurl_key(self):
        """
        Returns the TempURL key for the account
        """
        response = self.authed_request(method='HEAD')
        if 'x-account-meta-temp-url-key' not in response.headers:
            return None

        return response.headers['x-account-meta-temp-url-key']

    @behavior(ObjectStorageAPIClient)
    def _purge_container(self, container_name,
                         requestslib_kwargs=None):
        """
        @summary: List all the objects in a container and then attempt to
        delete them all. List the objects again and recursively call
        _purge_container if the container listing returns a 200 (indicating
        that there are still objects left).

        @param container_name: name of a container
        @type container_name: string
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
            self._purge_container(
                container_name, requestslib_kwargs=requestslib_kwargs)

    @behavior(ObjectStorageAPIClient)
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

        self._purge_container(
            container_name, requestslib_kwargs=requestslib_kwargs)

        delete_response = self.retry_until_success(
            self.client.delete_container,
            func_args=[container_name],
            func_kwargs={'requestslib_kwargs': requestslib_kwargs},
            success_func=success_func,
            max_retries=self.config.max_retry_count,
            sleep_time=self.config.retry_sleep_time)

        if delete_response.status_code == 409:
            raise Exception('Failed to force delete container {0} '
                            'with error code {1}'.format(
                                container_name,
                                delete_response.status_code))

    @behavior(ObjectStorageAPIClient)
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

    @behavior(ObjectStorageAPIClient)
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
