from unittest import TestCase
from httpretty import HTTPretty
from cloudcafe.identity.v2_0.extensions_api.client import ExtensionsAPI_Client

IDENTITY_ENDPOINT_URL = "http://localhost:35357"


class ExtensionsClientTest(TestCase):
    def setUp(self):
        self.url = IDENTITY_ENDPOINT_URL
        self.serialized_format = "json"
        self.deserialized_format = "json"
        self.auth_token = "AUTH_TOKEN"
        self.admin_extensions = "OS-KSADM"

        self.extensions_api_client = ExtensionsAPI_Client(
            url=self.url,
            auth_token=self.auth_token,
            serialized_format=self.serialized_format,
            deserialized_format=self.deserialized_format)

        self.role_id = "1"

        HTTPretty.enable()

    def test_list_extensions(self):
        url = "{0}/v2.0/extensions".format(self.url)
        HTTPretty.register_uri(HTTPretty.GET, url,
                               body=self._build_expected_body_response())
        actual_response = self.extensions_api_client.list_extensions()
        self._build_assertions(actual_response, url)

    def test_list_roles(self):
        url = "{0}/v2.0/{1}/roles".format(self.url, self.admin_extensions)
        HTTPretty.register_uri(HTTPretty.GET, url,
                               body=self._build_create_role_response())
        actual_response = self.extensions_api_client.list_roles()
        self._build_assertions(actual_response, url)

    def test_create_role(self):
        url = "{0}/v2.0/{1}/roles".format(self.url, self.admin_extensions)
        HTTPretty.register_uri(
            HTTPretty.POST, url,
            body=self._build_create_role_response())
        actual_response = self.extensions_api_client.create_role()
        self._build_assertions(actual_response, url)

    def test_delete_role(self):
        url = "{0}/v2.0/{1}/roles/{2}".format(self.url, self.admin_extensions,
                                              self.role_id)
        HTTPretty.register_uri(HTTPretty.DELETE, url)
        actual_response = self.extensions_api_client.delete_role(
            role_id=self.role_id)
        self._build_assertions(actual_response, url)

    def _build_assertions(self, actual_response, url):
        assert HTTPretty.last_request.headers['Content-Type'] == \
            'application/{0}'.format(self.serialized_format)
        assert HTTPretty.last_request.headers['Accept'] == \
            'application/{0}'.format(self.deserialized_format)
        assert HTTPretty.last_request.headers[
            'X-Auth-Token'] == self.auth_token
        assert 200 == actual_response.status_code
        assert url == actual_response.url

    def _build_expected_body_response(self):
        return {"extensions": [{"values": [
            {"updated": "2011-08-19T13:25:27-06:00",
             "name": "Openstack Keystone Admin",
             "links": {"href": "https://github.com/openstack/identity-api",
                       "type": "text/html", "rel": "describedby"},
             "namespace": "http://docs.openstack"
                          ".org/identity/api/ext/OS-KSADM/v1.0",
             "alias": "OS-KSADM",
             "description": "Openstack extensions to Keystone "
                            "v2.0 API enabling Admin Operations."}]}]}

    def _build_create_role_response(self):
        return {"role": {"id": "25dfade062ca486ebdb4e00246c40441",
                         "name": "response-test-221460"}}
