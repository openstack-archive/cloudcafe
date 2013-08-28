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

from cafe.engine.behaviors import BaseBehavior, behavior
from cloudcafe.common.tools import randomstring
from cloudcafe.objectstorage.objectstorage_api.config \
    import ObjectStorageAPIConfig
from cloudcafe.objectstorage.objectstorage_api.client \
    import ObjectStorageAPIClient


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
        self.client = client
        if config:
            self.config = config
        else:
            self.config = ObjectStorageAPIConfig()

    def generate_unique_container_name(self, identifier=None):
        if identifier:
            identifier = '{0}_'.format(identifier)

        container_name = '{0}({1}{2})'.format(
            self.config.base_container_name, identifier,
            randomstring.get_random_string())

        return container_name

    @behavior(ObjectStorageAPIClient)
    def create_container(self, name=None):
        response = self.client.create_container(name)
        if not response.ok:
            raise Exception('could not create container')

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
