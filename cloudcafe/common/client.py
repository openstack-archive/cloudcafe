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

REQUEST_CLASS = 0
RESPONSE_CLASS = 1


def setup_rest_operation(client_function):
    """
    @summary: Decorator to setup the execution of a rest operation on an
     API by generalized methods defined by BaseClient
    @param client_function: The function that will invoke one of the
     generalized methods defined by BaseClient
    @type client_function: Function
    @return: _execute: Function that sets up the rest api operation execution
    @rtype: Function
    """
    def _execute(self, *args, **kwargs):
        """
        @summary: Determines the operation to be executed and set up its
         execution by one the the generalized methods defined by BaseClient on
         behalf of a client function
        @param args: Postional arguments to be passed to the client function
        @type args: List
        @param kwargs: Key word arguments to be passed to the client function
        @type args: Dictionary
        @return: resp: ReST API response
        @rtype: Requests.response
        """
        pos = client_function.__name__.index('_')
        self.resource = client_function.__name__[pos + 1:]
        operation = client_function.__name__[:pos]
        if operation != 'list':
            self.resource = self._pluralize(self.resource)
        if self.resource not in self._models_classes.keys():
            raise NotImplementedError(
                'Resource {0} not implemented'.format(self.resource))
        self.request_class = self._models_classes[self.resource][REQUEST_CLASS]
        self.response_class =\
            self._models_classes[self.resource][RESPONSE_CLASS]
        resp = client_function(self, *args, **kwargs)
        self.resource = None
        self.request_class = None
        self.response_class = None
        return resp

    return _execute


class BaseClient(AutoMarshallingHTTPClient):
    """ This class defines a ReST client with generic operations for resources
    in an API. The assumptions are:

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

    In order to use this class, the developer has to inherit it and in the
    derived client:

    1) Populate the _models_classes dictionary. Each key / value pair has the
       following format:

        key: the plural name of the resource, 'networks' in the example we have
        been using

        value: a 2-tuple, where the first item points to requests class in the
        models for the resource. The second item points to the responses class

    2) Populate the _resource_plural_map dictionary, which is used to construct
       the plural name of a resource for those exceptions where it is not name
       + 's'. The dictionary only contains entries for the exceptions. Eack key
       / value pair has the following format:

        key: the resource name, for example 'policy'
        value: the plural. In the case of 'policy' it would be 'policies'

    3) Provide methods for the resources in the API that conform to the
       following name pattern: list_<resource_name>s, delete_<resource_name>,
       show_<resource_name>, create_<resource_name>, update_<resource_name>.
       The methods have to be annotated with the setup_rest_operation decorator
       provided in this module. The methods consist only of one line, which is
       a call to the corresponding method in this class, according to the
       operation to be performed. Finally, the methods can receive their
       arguments in any format convenient for the developer, but have to pass
       them to their counterpart in this class conforming to the signatures
       shown above in this doc string. An example using 'networks' as the
       resource and 'update' as the operation is:

       @setup_rest_operation
       update_network(self, network_id, name, **kwargs):
           return self._create(network_id, name=name, **kwargs)

    The derived client can handle resources and operations that do not conform
    to the assumptions made in this class. The developer only needs to provide
    the necessary methods in the derived client
    """

    _models_classes = {}

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
        self.resource = None
        self.request_class = None
        self.response_class = None

    def _pluralize(self, resource_name):
        """
        @summary: Returns the correct plural for a given resource name
        @param resource_name: Resource name to pluralize
        @type resource_name: String
        @return: name pluralized
        @rtype: String
        """
        return self._resource_plural_map.get(
            resource_name, '{0}s'.format(resource_name))

    def _list(self, **kwargs):
        """
        @summary: Executes a list operation for the given resource name in a
           ReST api
        @param kwargs: Key / value pairs specifiying the filters to be
           applied to the list operation. One of the keys can be
           'requestslib_kwargs', whose corresponding value is a dictionary
           that will be passed to the requests Python library as keywords
           arguments
        @type kwargs: Dictionary
        @return: resp: ReST API response
        @rtype: Requests.response
        """
        if 'requestslib_kwargs' in kwargs.keys():
            requestslib_kwargs = kwargs.pop('requestslib_kwargs')
        url = '{base_url}/{resource}'.format(base_url=self.url,
                                             resource=self.resource)
        resp = self.request('GET', url, params=kwargs,
                            response_entity_type=self.response_class,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def _delete(self, resource_id, requestslib_kwargs=None):
        """
        @summary: Executes a delete operation for the given resource name
           in the ReST api
        @param resource_id: the uuid of the resource to be deleted
        @type resource_id: String
        @param requestslib_kwargs: Key / value pairs to be passed to the
           requests Python library as keyword arguments
        @type kwargs: Dictionary
        @return: resp: ReST API response
        @rtype: Requests.response
        """
        url = '{base_url}/{resource}/{resource_id}'.format(
            base_url=self.url, resource=self.resource, resource_id=resource_id)
        resp = self.request('DELETE', url,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def _show(self, resource_id, requestslib_kwargs=None):
        """
        @summary: Executes a show operation for the given resource name
           in the ReST api
        @param resource_id: the uuid of the resource to be shown
        @type resource_id: String
        @param requestslib_kwargs: Key / value pairs to be passed to the
           requests Python library as keyword arguments
        @type kwargs: Dictionary
        @return: resp: ReST API response
        @rtype: Requests.response
        """
        url = '{base_url}/{resource}/{resource_id}'.format(
            base_url=self.url, resource=self.resource, resource_id=resource_id)
        resp = self.request('GET', url,
                            response_entity_type=self.response_class,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def _create(self, **kwargs):
        """
        @summary: Executes a create operation for the given resource name
           in the ReST api
        @param kwargs: Key / value pairs specifiying the attributes of the
           resource to be created by the ReST API. One of the keys can be
           'requestslib_kwargs', whose corresponding value is a dictionary
           that will be passed to the requests Python library as keywords
           arguments
        @type kwargs: Dictionary
        @return: resp: ReST API response
        @rtype: Requests.response
        """
        if 'requestslib_kwargs' in kwargs.keys():
            requestslib_kwargs = kwargs.pop('requestslib_kwargs')
        request_object = self.request_class(**kwargs)
        url = '{base_url}/{resource}'.format(base_url=self.url,
                                             resource=self.resource)
        resp = self.request('POST', url,
                            response_entity_type=self.response_class,
                            request_entity=request_object,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def _update(self, resource_id, **kwargs):
        """
        @summary: Executes an update operation for the given resource name
           in the ReST api
        @param resource_id: the uuid of the resource to be updated
        @type resource_id: String
        @param kwargs: Key / value pairs specifiying the attributes to be
           updated for the specified resource by the ReST API. One of the
           keys can be 'requestslib_kwargs', whose corresponding value is
           a dictionary that will be passed to the requests Python library
           as keywords arguments
        @type kwargs: Dictionary
        @return: resp: ReST API response
        @rtype: Requests.response
        """
        if 'requestslib_kwargs' in kwargs.keys():
            requestslib_kwargs = kwargs.pop('requestslib_kwargs')
        request_object = self.request_class(**kwargs)
        url = '{base_url}/{resource}/{resource_id}'.format(
            base_url=self.url, resource=self.resource, resource_id=resource_id)
        resp = self.request('PUT', url,
                            response_entity_type=self.response_class,
                            request_entity=request_object,
                            requestslib_kwargs=requestslib_kwargs)
        return resp
