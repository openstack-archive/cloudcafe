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
import datetime
import uuid
import json
from copy import deepcopy
from time import sleep

from cafe.engine.behaviors import BaseBehavior, behavior
from cloudcafe.objectstorage.objectstorage_api.config \
    import ObjectStorageAPIConfig
from cloudcafe.objectstorage.objectstorage_api.client \
    import ObjectStorageAPIClient


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

    def retry_until_success(self, func, func_args=None, func_kwargs=None,
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

        if self.config.list_timeout:
            stop_time = (datetime.datetime.now() +
                         datetime.timedelta(seconds=timeout))

        def default_success_func(response):
            return response.ok
        success_func = success_func or default_success_func

        response = None
        reached_timeout = False
        while not reached_timeout:
            response = None

            if not timeout:
                reached_timeout = True
            else:
                reached_timeout = datetime.datetime.now() >= stop_time

            if sleep_seconds == 0:
                sleep_seconds = 1
            else:
                sleep(sleep_seconds)
                sleep_seconds = sleep_seconds * 2

            response = func(*func_args, **func_kwargs)
            if response:
                if success_func(response):
                    return response
            else:
                raise ObjectStorageAPIBehaviorException('invalid response')
        if response.ok:
            # If the response came back successful, but the success condition
            # did not occur, then return the response anyway so the caller
            # can deal with how to handle the situation.
            return response
        raise ObjectStorageAPIBehaviorException(
            'Unable to satisfy success condition.', response)

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
    def create_container(self, container_name, log_delivery=False, headers={}):

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
            timeout=self.config.list_timeout)
        return response.entity

    @behavior(ObjectStorageAPIClient)
    def create_object(self, container_name, object_name, data=None,
                      headers={}, params={}):
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
            timeout=self.config.list_timeout)
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
        @summary: deletes all the objects in a container and then deletes
                  the container
        @param container_name: name of a container
        @type container_name: string
        @rtype: delete container response
        """
        params = {'format': 'json'}
        response = self.client.list_objects(
            container_name,
            params=params,
            requestslib_kwargs=requestslib_kwargs)

        for storage_object in response.entity:
            self.client.delete_object(
                container_name,
                storage_object.name)

        return self.client.delete_container(container_name)

    def force_delete_containers(self, container_list,
                                requestslib_kwargs=None):
        """
        @summary: Calls purge container on a list of containers
        @param container_list: a list of containers
        @type container_list: list
        """
        for container_name in container_list:
            resp = self._purge_container(
                container_name,
                requestslib_kwargs=requestslib_kwargs)

            if not resp.ok:
                self._log.debug("force delete failure {0} status {1}".format(
                    container_name,
                    resp.status_code))
