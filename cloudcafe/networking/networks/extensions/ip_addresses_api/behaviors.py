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

from cloudcafe.networking.networks.common.behaviors \
    import NetworkingBaseBehaviors
from cloudcafe.networking.networks.extensions.ip_addresses_api.constants \
    import IPAddressesResource, IPAddressesResponseCodes


class IPAddressesBehaviors(NetworkingBaseBehaviors):

    def __init__(self, ip_addresses_client, ip_addresses_config):
        super(IPAddressesBehaviors, self).__init__()
        self.config = ip_addresses_config
        self.client = ip_addresses_client
        self.response_codes = IPAddressesResponseCodes
        self.ip_address_resource = IPAddressesResource(
            IPAddressesResource.IP_ADDRESS)

    def create_ip_address(self, network_id=None, version=None, device_ids=None,
                          port_ids=None, resource_build_attempts=None,
                          raise_exception=True, poll_interval=None):
        """
        @summary: Creates an IP address on a specified network
            A list of device_ids may be optionally specified to create the IP
            address and added to their respective ports. A list of port_ids may
            be optionally specified to create the IP address and added to the
            specified ports. At least one of device_ids or port_ids must be
            specified.
        @param network_id: network UUID to get the IP address from
        @type network_id: str
        @param version: IP address version 4 or 6
        @type version: int
        @param device_ids (optional): server UUIDs to add the IP address to
            their respective ports on the given network
        @type device_ids: list
        @param port_ids(optional): port UUIDs to add the IP address on the
            given network
        @type port_ids: list
        @param resource_build_attempts: number of API retries
        @type resource_build_attempts: int
        @param raise_exception: flag to raise an exception if the
            Network was not created or to return None
        @type raise_exception: bool
        @param poll_interval: sleep time interval between API retries
        @type poll_interval: int
        @return: NetworkingResponse object with api response and failure list
        @rtype: common.behaviors.NetworkingResponse
        """
        attrs_kwargs = dict(network_id=network_id, version=version,
                            device_ids=device_ids, port_ids=port_ids)

        result = self._create_resource(
            resource=self.ip_address_resource,
            resource_build_attempts=resource_build_attempts,
            raise_exception=raise_exception, poll_interval=poll_interval,
            has_name=False, attrs_kwargs=attrs_kwargs)

        return result

    def update_ip_address(self, ip_address_id, port_ids=None,
                          resource_update_attempts=None, raise_exception=False,
                          poll_interval=None):
        """
        @summary: Update an IP address, ex. to change ports.
            This will eliminate any previous associations to ports.
        @param ip_address_id: The UUID for the ip_address
        @type ip_address_id: str
        @param port_ids: port UUIDs to associate to the IP address
        @param resource_update_attempts: number of API retries
        @type resource_update_attempts: int
        @param raise_exception: flag to raise an exception if the
            Network was not updated or to return None
        @type raise_exception: bool
        @param poll_interval: sleep time interval between API retries
        @type poll_interval: int
        @return: NetworkingResponse object with api response and failure list
        @rtype: common.behaviors.NetworkingResponse
        """
        attrs_kwargs = dict(port_ids=port_ids)

        result = self._update_resource(
            resource=self.ip_address_resource, resource_id=ip_address_id,
            resource_update_attempts=resource_update_attempts,
            raise_exception=raise_exception, poll_interval=poll_interval,
            attrs_kwargs=attrs_kwargs)

        return result

    def get_ip_address(self, ip_address_id, resource_get_attempts=None,
                       raise_exception=False, poll_interval=None):
        """
        @summary: Shows a specific IP address
        @param ip_address_id: The UUID for the ip_address
        @type ip_address_id: str
        @param resource_get_attempts: number of API retries
        @type resource_get_attempts: int
        @param raise_exception: flag to raise an exception if the get
            Network was not as expected or to return None
        @type raise_exception: bool
        @param poll_interval: sleep time interval between API retries
        @type poll_interval: int
        @return: NetworkingResponse object with api response and failure list
        @rtype: common.behaviors.NetworkingResponse
        """
        result = self._get_resource(
            resource=self.ip_address_resource, resource_id=ip_address_id,
            resource_get_attempts=resource_get_attempts,
            raise_exception=raise_exception, poll_interval=poll_interval)

        return result

    def list_ip_addresses(self, ip_address_id=None, network_id=None,
                          address=None, subnet_id=None, port_ids=None,
                          tenant_id=None, version=None, type_=None,
                          port_id=None, device_id=None, service=None,
                          limit=None, marker=None, page_reverse=None,
                          resource_list_attempts=None, raise_exception=False,
                          poll_interval=None):
        """
        @summary: Lists IP addresses, filtered by params if given
        @param ip_address_id: shared IP UUID
        @type ip_address_id: str
        @param network_id: network UUID where the IP address belongs to
        @type network_id: str
        @param address: IP address
        @type address: str
        @param subnet_id: subnet UUID where the IP address belongs to
        @type subnet_id: str
        @param port_ids: IP addresses port UUIDs
        @type port_ids: list
        @param tenant_id: tenant ID of the shared IP user
        @type tenant_id: str
        @param version: IP address version 4 or 6
        @type version: int
        @param type_: IP address type, for ex. fixed
        @type type_: str
        @param port_id: IP address by their port ID
        @type port_id: str (/ip_addresses/{id}/ports child resource attr)
        @param device_id: IP address by their port device ID
        @type device_id: str (/ip_addresses/{id}/ports child resource attr)
        @param service: IP address by their port service, for ex. compute
        @type service: str (/ip_addresses/{id}/ports child resource attr)
        @param limit: page size
        @type limit: int
        @param marker: Id of the last item of the previous page
        @type marker: string
        @param page_reverse: direction of the page
        @type page_reverse: bool
        @param resource_list_attempts: number of API retries
        @type resource_list_attempts: int
        @param raise_exception: flag to raise an exception if the list
            Network was not as expected or to return None
        @type raise_exception: bool
        @param poll_interval: sleep time interval between API retries
        @type poll_interval: int
        @return: NetworkingResponse object with api response and failure list
        @rtype: common.behaviors.NetworkingResponse
        """
        params_kwargs = dict(
            ip_address_id=ip_address_id, network_id=network_id,
            address=address, subnet_id=subnet_id, port_ids=port_ids,
            tenant_id=tenant_id, version=version, type_=type_, port_id=port_id,
            device_id=device_id, service=service, limit=limit, marker=marker,
            page_reverse=page_reverse)

        result = self._list_resources(
            resource=self.ip_address_resource,
            resource_list_attempts=resource_list_attempts,
            raise_exception=raise_exception, poll_interval=poll_interval,
            params_kwargs=params_kwargs)

        return result

    def delete_ip_address(self, ip_address_id, resource_delete_attempts=None,
                          raise_exception=False, poll_interval=None):
        """
        @summary: Deletes a specified IP address
        @param ip_address_id: The UUID for the ip_address to delete
        @type ip_address_id: str
        @param resource_delete_attempts: number of API retries
        @type resource_delete_attempts: int
        @param raise_exception: flag to raise an exception if the deleted
            Network was not as expected or to return None
        @type raise_exception: bool
        @param poll_interval: sleep time interval between API retries
        @type poll_interval: int
        @return: NetworkingResponse object with api response and failure list
        @rtype: common.behaviors.NetworkingResponse
        """
        result = self._delete_resource(
            resource=self.ip_address_resource,
            resource_id=ip_address_id,
            resource_delete_attempts=resource_delete_attempts,
            raise_exception=raise_exception, poll_interval=poll_interval)

        return result

    def delete_ip_addresses(self, ip_address_list=None, tenant_id=None,
                            skip_delete=None):
        """
        @summary: deletes multiple IP Addresses
        @param ip_address_list: list of IP Address UUIDs
        @type ip_address_list: list(str)
        @param tenant_id: IP Address tenant ID to filter by
        @type tenant_id: string (ignored if ip_address_list given)
        @param skip_delete: list of IP Address UUIDs that should skip deletion
        @type skip_delete: list
        @return: failed deletes list with IP Address IDs and failures
        @rtype: list(dict)
        """

        # If IP address list not given, deleting all shared IPs
        if not ip_address_list:
            resp = self.list_ip_addresses(type_='shared', raise_exception=True)
            shared_ips = resp.response.entity
            ip_address_list = self.get_id_list_from_entity_list(
                entity_list=shared_ips)

        result = self._delete_resources(
            resource=self.ip_address_resource,
            resource_list=ip_address_list,
            tenant_id=tenant_id, skip_delete=skip_delete)

        return result

    def clean_ip_address(self, ip_address_id, timeout=None,
                         poll_interval=None):
        """
        @summary: deletes an IP Address within a time out
        @param ip_address_id: The UUID for the ip_address to delete
        @type ip_address_id: str
        @param timeout: seconds to wait for the IP Address to be deleted
        @type timeout: int
        @param poll_interval: sleep time interval between API delete/get calls
        @type poll_interval: int
        @return: None if delete was successful or the undeleted ip_address_id
        @rtype: None or string
        """
        result = self._clean_resource(
            resource=self.ip_address_resource,
            resource_id=ip_address_id,
            timeout=timeout, poll_interval=poll_interval)

        return result

    def clean_ip_addresses(self, ip_address_list, timeout=None,
                           poll_interval=None):
        """
        @summary: deletes each IP Address from a list calling clean_ip_address
        @param ip_address_list: list of IP Address UUIDs
        @type ip_address_list: list(str)
        @param timeout: seconds to wait for the IP Address to be deleted
        @type timeout: int
        @param poll_interval: sleep time interval between API delete/get calls
        @type poll_interval: int
        @return: list of undeleted IP Address UUIDs
        @rtype: list(str)
        """
        result = self._clean_resources(
            resource=self.ip_address_resource,
            resource_list=ip_address_list,
            timeout=timeout, poll_interval=poll_interval)

        return result
