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
from copy import deepcopy
import uuid
import json

from cafe.engine.behaviors import BaseBehavior, behavior
from cloudcafe.objectstorage.objectstorage_api.config \
    import ObjectStorageAPIConfig
from cloudcafe.objectstorage.objectstorage_api.client \
    import ObjectStorageAPIClient


class ObjectStorageAPIBehaviorException(Exception):
    pass


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

    def generate_unique_container_name(self, identifier=None):
        if identifier:
            identifier = '{0}_'.format(identifier)

        randomstring = str(uuid.uuid4()).replace('-', '')

        container_name = '{0}_{1}{2}'.format(
            self.config.base_container_name, identifier,
            randomstring)

        return container_name

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
        Returns a string represnting the enabled features seperated by commas.
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
