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

from httpretty import HTTPretty

from metatests.cloudcafe.networking.fixtures import ClientTestFixture


class BaseNetworkingTest(ClientTestFixture):

    @classmethod
    def setUpClass(cls):
        super(BaseNetworkingTest, cls).setUpClass()
        cls.client = None

    def _execute(self, api_method, http_method, resource_singular,
                 resource_id=None, response_class=None,
                 expected_request_body=None, expected_status_code=200,
                 **kwargs):
        uri = "{0}/{1}s".format(self.NETWORKING_API_ENDPOINT,
                                resource_singular)
        if resource_id:
            uri = "{0}/{1}".format(uri, resource_id)
        if response_class:
            response = response_class(self.FORMAT)
            get_response_method = getattr(
                response, "_get_{0}".format(resource_singular))
            HTTPretty.register_uri(http_method, uri,
                                   body=get_response_method(),
                                   status=expected_status_code)
        else:
            HTTPretty.register_uri(http_method, uri,
                                   status=expected_status_code)
        actual_response = api_method(**kwargs)
        self._assert_default_headers_in_request(HTTPretty.last_request)
        self.assertEqual(expected_status_code, actual_response.status_code)
        if expected_request_body:
            self.assertEqual(HTTPretty.last_request.body,
                             expected_request_body)
        if response_class:
            self.assertEqual(get_response_method(), actual_response.content)

    def _test_create(self, resource_singular, response_class,
                     expected_request_body, expected_status_code=201,
                     **kwargs):
        api_method = getattr(self.client,
                             "create_{0}".format(resource_singular))
        self._execute(api_method, HTTPretty.POST, resource_singular,
                      response_class=response_class,
                      expected_request_body=expected_request_body,
                      expected_status_code=expected_status_code, **kwargs)

    def _test_update(self, resource_singular, resource_id, response_class,
                     expected_request_body, expected_status_code=200,
                     **kwargs):
        api_method = getattr(self.client,
                             "update_{0}".format(resource_singular))
        self._execute(api_method, HTTPretty.PUT, resource_singular,
                      resource_id=resource_id, response_class=response_class,
                      expected_request_body=expected_request_body,
                      expected_status_code=expected_status_code, **kwargs)

    def _test_list(self, resource_singular, response_class,
                   expected_status_code=200, **kwargs):
        api_method = getattr(self.client,
                             "list_{0}s".format(resource_singular))
        self._execute(api_method, HTTPretty.GET, resource_singular,
                      response_class=response_class,
                      expected_status_code=expected_status_code, **kwargs)

    def _test_show(self, resource_singular, resource_id, response_class,
                   expected_status_code=200, **kwargs):
        api_method = getattr(self.client,
                             "show_{0}".format(resource_singular))
        self._execute(api_method, HTTPretty.GET, resource_singular,
                      resource_id=resource_id, response_class=response_class,
                      expected_status_code=expected_status_code, **kwargs)

    def _test_delete(self, resource_singular, resource_id,
                     expected_status_code=204, **kwargs):
        api_method = getattr(self.client,
                             "delete_{0}".format(resource_singular))
        self._execute(api_method, HTTPretty.DELETE, resource_singular,
                      resource_id=resource_id,
                      expected_status_code=expected_status_code, **kwargs)
