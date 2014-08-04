"""
Copyright 2014 Rackspace

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

from cafe.engine.http.client import AutoMarshallingHTTPClient
from cloudcafe.common.exceptions import AttributeException,\
    NotImplementedException

REQUEST_CLASS = 0
RESPONSE_CLASS = 1


class BaseClient(AutoMarshallingHTTPClient):
    """ This class defines a generic ReST client that dinamically generates
    calls for resources in an API. The assumptions are:

    1) Each resource has the following operations (or a subset thereof):
    create, list, show, update and delete

    2) The calls to the resources operations can be made with the following
    signatures (using 'networks' as an example resource):

        list_networks(**kwargs) where **kwargs contains the filtering arguments
        and optionally requestslib_kwargs

        delete_network(network_id, requestslib_kwargs=requestslib_kwargs)

        show_network(network_id, requestslib_kwargs=requestslib_kwargs)

        create_network(**kwargs) where **kwargs contains the request arguments
        and optionally requestslib_kwargs

        update_network(network_id, **kwargs) where **kwargs contains the
        request arguments and optionally requestslib_kwargs

    In order to use this class, the developer has to inherit it and populate
    the following 2 dictionaries:

    1) _models_classes. Each key / value pair has the following format:

        key: the plural name of the resource, 'networks' in the example we have
        been using

        value: a 2-tuple, where the first item points to requests class in the
        models for the resource. The second item points to the responses class

    2) _resource_plural_map. Dictionary used to construct the plural name of a
    resource for those exceptions where it is not name + 's'. The dictionary
    only contains entries for the exceptions. Eack key / value pair has the
    following format:

        key: the resource name, for example 'policy'
        value: the plural. In the case of 'policy' it would be 'policies'

    The core of this client is the __getattr__ method. It is called by the
    Python run-time when an object's attribute is accesed and it is not
    defined. In the case of this client, __getattr__ will receive as an
    argument the name of the operation being invoked on an API resource, i.e.
    'list_networks' as an example. The __getattr__ in this client uses the
    operation name to dynamically generate the corresponding method using
    _lister, _shower, _deleter, _creater and _updater defined below
    """

    _models_classes = None

    # map from resource name to a plural name
    # needed only for those which can't be constructed as name + 's'
    _resource_plural_map = {}

    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None):
        """
        @param url: Base URL for the service
        @type url: String
        @param auth_token: Auth token to be used for all requests
        @type auth_token: String
        @param serialize_format: Format for serializing requests
        @type serialize_format: String
        @param deserialize_format: Format for de-serializing responses
        @type deserialize_format: String
        """
        super(BaseClient, self).__init__(serialize_format,
                                         deserialize_format)
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        ct = '{content_type}/{content_subtype}'.format(
            content_type='application',
            content_subtype=self.serialize_format)
        accept = '{content_type}/{content_subtype}'.format(
            content_type='application',
            content_subtype=self.deserialize_format)
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept
        self.url = url

    def _pluralize(self, resource_name):
        # get plural from map or just add 's'
        return self._resource_plural_map.get(
            resource_name, '{0}s'.format(resource_name))

    def _lister(self, plural_name):
        def _list(**kwargs):
            if plural_name not in self._models_classes.keys():
                raise NotImplementedException(
                    'Resource {0} not implemented'.format(plural_name))
            if 'requestslib_kwargs' in kwargs.keys():
                requestslib_kwargs = kwargs.pop('requestslib_kwargs')
            url = '{base_url}/{plural_name}'.format(base_url=self.url,
                                                    plural_name=plural_name)
            response_class = self._models_classes[plural_name][RESPONSE_CLASS]
            resp = self.request('GET', url, params=kwargs,
                                response_entity_type=response_class,
                                requestslib_kwargs=requestslib_kwargs)
            return resp

        return _list

    def _deleter(self, resource_name):
        def _delete(resource_id, requestslib_kwargs=None):
            plural = self._pluralize(resource_name)
            if plural not in self._models_classes.keys():
                raise NotImplementedException(
                    'Resource {0} not implemented'.format(plural))
            url = '{base_url}/{plural}/{resource_id}'.format(
                base_url=self.url, plural=plural, resource_id=resource_id)
            resp = self.request('DELETE', url,
                                requestslib_kwargs=requestslib_kwargs)
            return resp

        return _delete

    def _shower(self, resource_name):
        def _show(resource_id, requestslib_kwargs=None):
            plural = self._pluralize(resource_name)
            if plural not in self._models_classes.keys():
                raise NotImplementedException(
                    'Resource {0} not implemented'.format(plural))
            url = '{base_url}/{plural}/{resource_id}'.format(
                base_url=self.url, plural=plural, resource_id=resource_id)
            response_class = self._models_classes[plural][RESPONSE_CLASS]
            resp = self.request('GET', url,
                                response_entity_type=response_class,
                                requestslib_kwargs=requestslib_kwargs)
            return resp

        return _show

    def _creater(self, resource_name):
        def _create(**kwargs):
            plural = self._pluralize(resource_name)
            if plural not in self._models_classes.keys():
                raise NotImplementedException(
                    'Resource {0} not implemented'.format(plural))
            if 'requestslib_kwargs' in kwargs.keys():
                requestslib_kwargs = kwargs.pop('requestslib_kwargs')
            request_object =\
                self._models_classes[plural][REQUEST_CLASS](**kwargs)
            response_class = self._models_classes[plural][RESPONSE_CLASS]
            url = '{base_url}/{plural}'.format(base_url=self.url,
                                               plural=plural)
            resp = self.request('POST', url,
                                response_entity_type=response_class,
                                request_entity=request_object,
                                requestslib_kwargs=requestslib_kwargs)
            return resp

        return _create

    def _updater(self, resource_name):
        def _update(resource_id, **kwargs):
            plural = self._pluralize(resource_name)
            if plural not in self._models_classes.keys():
                raise NotImplementedException(
                    'Resource {0} not implemented'.format(plural))
            if 'requestslib_kwargs' in kwargs.keys():
                requestslib_kwargs = kwargs.pop('requestslib_kwargs')
            request_object =\
                self._models_classes[plural][REQUEST_CLASS](**kwargs)
            response_class = self._models_classes[plural][RESPONSE_CLASS]
            url = '{base_url}/{plural}/{resource_id}'.format(
                base_url=self.url, plural=plural, resource_id=resource_id)
            resp = self.request('PUT', url,
                                response_entity_type=response_class,
                                request_entity=request_object,
                                requestslib_kwargs=requestslib_kwargs)
            return resp

        return _update

    def __getattr__(self, name):
        """
        @param name: The API operation to be executed by the client, i.e.
          'list_networks' for example
        @type url: String
        @return: The method that will handle the API operation. This method is
           generated dinamically by the _lister, _deleter, _shower, _creater
           and _updater methods above
        @rtype: method
        """
        method_prefixes = ["list_", "delete_", "show_", "create_", "update_"]
        method_functors = [self._lister,
                           self._deleter,
                           self._shower,
                           self._creater,
                           self._updater]
        for index, prefix in enumerate(method_prefixes):
            prefix_len = len(prefix)
            if name[:prefix_len] == prefix:
                return method_functors[index](name[prefix_len:])
        raise AttributeException(name)
