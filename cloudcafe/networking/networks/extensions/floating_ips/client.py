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

from cafe.engine.http.client import AutoMarshallingHTTPClient

from cloudcafe.networking.networks.extensions.floating_ips.models.request \
    import FloatingIPRequest, FloatingIPUpdate
from cloudcafe.networking.networks.extensions.floating_ips.models.response \
    import FloatingIPInfo, FloatingIPInfoList


CONTENT_TYPE_FORMAT = '{content_type}/{content_subtype}'


class FloatingIPClient(AutoMarshallingHTTPClient):
    def __init__(self, url, auth_token, serialize_format='json',
                 deserialize_format='json', tenant_id=None):
        """
        Instantiate a Floating IP Client for the neutron floatingip extension.

        :param url: (REQUIRED) The base end point without the floatingip
                  qualifier.
        :param auth_token: (REQUIRED) The authentication token
        :param serialize_format: (OPTIONAL) Format to serialize from
                  (DEFAULT: 'json')
        :param deserialize_format: (OPTIONAL) Format to deserialize from
                  (DEFAULT: 'json')
        :param tenant_id: (OPTIONAL) UUID representing the tenant.

        :return: None

        """
        super(FloatingIPClient, self).__init__(serialize_format,
                                               deserialize_format)
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = self.auth_token

        self.default_headers['Content-Type'] = CONTENT_TYPE_FORMAT.format(
            content_type='application',
            content_subtype=self.serialize_format)

        self.default_headers['Accept'] = CONTENT_TYPE_FORMAT.format(
            content_type='application',
            content_subtype=self.deserialize_format)

        if tenant_id:
            self.default_headers['X-Auth-Project-Id'] = tenant_id

        self.base_url = url
        self.floating_ip_url = '{0}/floatingips'.format(self.base_url)

    def create_floating_ip(self, floating_network_id, floating_ip_address=None,
                           tenant_id=None, fixed_ip_address=None, port_id=None,
                           requestslib_kwargs=None):
        """
        To associate the floating IP with an internal port, specify the port ID
        attribute in the request body. If you do not specify a port ID in the
        request, you can issue a PUT request instead of a POST request. You can
        create floating IPs on external networks only.

        :param floating_network_id: (REQUIRED) - UUID for floating IP network.
        :param floating_ip_address: (OPTIONAL) - The floating IP address.
                 If not specified, system will assign an IP address from the
                 floating IP network specified by the floating IP network id.
        :param tenant_id: (OPTIONAL) - Tenant ID (Only admins can specify an ID
                 other than their own.)
        :param fixed_ip_address: (OPTIONAL) - The fixed IP address associated
                 with the floating IP. If you intend to associate the floating
                 IP with a fixed IP at creation time, then you must indicate
                 the identifier of the internal port. If an internal port has
                 multiple associated IP addresses, the service chooses the
                 first IP unless you explicitly specify the parameter
                 fixed_ip_address to select a specific IP.
        :param port_id: (OPTIONAL) - The port ID.
        :param requestslib_kwargs: (OPTIONAL) - Extra information needed by
                 client

        :return: FloatingIPInfo Response object

        """
        method = 'POST'
        url = self.floating_ip_url
        request = FloatingIPRequest(floating_network_id=floating_network_id,
                                    floating_ip_address=floating_ip_address,
                                    fixed_ip_address=fixed_ip_address,
                                    tenant_id=tenant_id, port_id=port_id)

        return self.request(method, url,
                            request_entity=request,
                            response_entity_type=FloatingIPInfo,
                            requestslib_kwargs=requestslib_kwargs)

    def associate_floating_ip(self, floating_ip_id, port_id=None,
                              requestslib_kwargs=None):
        """
        The association process is the same as the process for the create
        floating IP operation. To disassociate a floating IP from a port, set
        the port_id attribute to null or omit it from the request body.

        :param floating_ip_id: (REQUIRED) - The UUID of the floating IP
        :param requestslib_kwargs: (OPTIONAL) - Extra information needed by
                 client

        :return: FloatingIPInfo Response Object

        """
        method = 'PUT'
        url = '{url}/{floating_ip_id}'.format(url=self.floating_ip_url,
                                              floating_ip_id=floating_ip_id)
        request = FloatingIPUpdate(port_id)
        return self.request(method, url,
                            request_entity=request,
                            response_entity_type=FloatingIPInfo,
                            requestslib_kwargs=requestslib_kwargs)

    def list_floating_ip_details(self, floating_ip_id, fixed_ip_address=False,
                                 floating_ip_address=False, status=False,
                                 floating_network_id=False, router_id=False,
                                 port_id=False, id_=False, tenant_id=False,
                                 requestslib_kwargs=None):
        """
        Show info about the specified floating IP id.

        :param floating_ip_id: (REQUIRED) - The UUID of the floating IP
        :param requestslib_kwargs: (OPTIONAL) - Extra information needed by
                 client

        Set the various fields to True to control which fields are returned in
        the response body. All parameters listed below are OPTIONAL and are
        BOOLEAN. Set to True to include the field in the response. If all
        fields are False, all fields will be included in the response.

        :param floating_network_id: Boolean
        :param fixed_ip_address: Boolean
        :param floating_ip_address: Boolean
        :param status: Boolean
        :param router_id: Boolean
        :param port_id: Boolean

        :return: FloatingIPInfo Response Object

        """
        if requestslib_kwargs is None:
            requestslib_kwargs = {}

        method = 'GET'
        url = '{url}/{floating_ip_id}'.format(url=self.floating_ip_url,
                                              floating_ip_id=floating_ip_id)

        # Determine if additional url params have been specified.
        filter_by = {
            'floating_ip_address': floating_ip_address, 'router_id': router_id,
            'fixed_ip_address': fixed_ip_address, 'status': status, 'id': id_,
            'floating_network_id': floating_network_id, 'port_id': port_id,
            'tenant_id': tenant_id,
        }

        fields = [field for field, value in filter_by.iteritems() if value]
        if fields:
            requestslib_kwargs.update({'fields': fields})

        return self.request(method, url,
                            response_entity_type=FloatingIPInfo,
                            requestslib_kwargs=requestslib_kwargs)

    def list_floating_ips(self, fixed_ip_address=False, status=False,
                          floating_ip_address=False, router_id=False,
                          port_id=False, id_=False, tenant_id=False,
                          floating_network_id=False,
                          requestslib_kwargs=None):
        """
        Default policy settings return only those floating IPs that are owned
        by the tenant who submits the request, unless an admin user submits the
        request.

        :param requestslib_kwargs: (OPTIONAL) - Extra information needed by
                 client

        Set the various fields to True to control which fields are returned in
        the response body. All parameters listed below are OPTIONAL and are
        BOOLEAN. Set to True to include the field in the response. If all
        fields are False, all fields will be included in the response.

        :param floating_network_id: Boolean
        :param fixed_ip_address: Boolean
        :param floating_ip_address: Boolean
        :param status: Boolean
        :param router_id: Boolean
        :param port_id: Boolean

        :return: FloatingIPInfo Response Object

        """
        if requestslib_kwargs is None:
            requestslib_kwargs = {}

        method = 'GET'
        url = self.floating_ip_url

        # Determine if additional url params have been specified.
        filter_by = {
            'floating_ip_address': floating_ip_address, 'router_id': router_id,
            'fixed_ip_address': fixed_ip_address, 'status': status, 'id': id_,
            'floating_network_id': floating_network_id, 'tenant_id': tenant_id,
            'port_id': port_id,
        }

        fields = [field for field, value in filter_by.iteritems() if value]
        if fields:
            requestslib_kwargs.update({'fields': fields})

        return self.request(method, url,
                            response_entity_type=FloatingIPInfoList,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_floating_ip(self, floating_ip_id, requestslib_kwargs):
        """
        Delete (release) the floating IP.

        :param floating_ip_id: (REQUIRED) UUID of floating IP address
        :param requestslib_kwargs: (OPTIONAL) - Extra information needed by
                 client

        :return: None

        """
        method = 'DELETE'
        url = '{url}/{ip}'.format(url=self.floating_ip_url, ip=floating_ip_id)
        return self.request(method, url, requestslib_kwargs=requestslib_kwargs)
