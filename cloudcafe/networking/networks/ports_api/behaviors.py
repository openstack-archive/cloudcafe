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
import netaddr

from cloudcafe.networking.networks.common.behaviors \
    import NetworkingBaseBehaviors
from cloudcafe.networking.networks.common.constants \
    import NeutronResponseCodes, NeutronResource
from cloudcafe.networking.networks.common.exceptions \
    import NetworkIDMissingException


class PortsBehaviors(NetworkingBaseBehaviors):

    def __init__(self, ports_client, ports_config):
        super(PortsBehaviors, self).__init__()
        self.config = ports_config
        self.client = ports_client
        self.response_codes = NeutronResponseCodes
        self.ports_resource = NeutronResource(NeutronResource.PORT)

    def get_subnet_ids_from_fixed_ips(self, fixed_ips):
        """
        @summary: gets the subnet ids from the port fixed IPs attribute
        @param fixed_ips: list of fixed_ips
        @type fixed_ips: list(dict)
        @return: subnet ids and errors lists from fixed IPs
        @rtype: dict
        """
        # Errors list will contain unexpected fixed IPs if any
        results = {'subnet_ids': [], 'errors': []}
        for fixed_ip in fixed_ips:
            if 'subnet_id' not in fixed_ip or fixed_ip['subnet_id'] is None:
                results['errors'].append(fixed_ip)
            else:
                results['subnet_ids'].append(fixed_ip['subnet_id'])
        return results

    def get_addresses_from_fixed_ips(self, fixed_ips, ip_version=4):
        """
        @summary: gets the IP addresses from the port fixed IPs attribute
        @param fixed_ips: list of fixed_ips
        @type fixed_ips: list(dict)
        @param version: IP version of addresses to get
        @type version: int
        @return: IP addresses from fixed IPs
        @rtype: list(str)
        """
        result = []
        for fixed_ip in fixed_ips:
            ip = netaddr.IPAddress(fixed_ip['ip_address'])
            if ip.version == ip_version:
                result.append(str(ip))
        return result

    def format_fixed_ips(self, fixed_ips):
        """
        @summary: formats fixed ips for assertions removing zeros on
            IPv6 addresses
        @param fixed_ips: list of fixed_ips
        @type fixed_ips: list(dict)
        @return: formated fixed_ips
        @rtype: list(dict)
        """
        result = [dict(subnet_id=fixed_ip['subnet_id'], ip_address=str(
            netaddr.IPAddress(fixed_ip['ip_address'])))
            for fixed_ip in fixed_ips]
        return result

    def create_port(self, network_id, name=None, admin_state_up=None,
                    mac_address=None, fixed_ips=None, device_id=None,
                    device_owner=None, tenant_id=None, security_groups=None,
                    resource_build_attempts=None, raise_exception=True,
                    use_exact_name=False, poll_interval=None,
                    timeout=None, use_over_limit_retry=False):
        """
        @summary: Creates and verifies a Port is created as expected
        @param network_id: network port is associated with (CRUD: CR)
        @type network_id: string
        @param name: human readable name for the port, may not be unique.
            (CRUD: CRU)
        @type name: string
        @param admin_state_up: true or false (default true), the admin state
            of the port. If down, the port does not forward packets (CRUD: CRU)
        @type admin_state_up: bool
        @param mac_address: mac address to use on the port (CRUD: CR)
        @type mac_address: string
        @param fixed_ips: ip addresses for the port associating the
            port with the subnets where the IPs come from (CRUD: CRU)
        @type fixed_ips: list(dict)
        @param device_id: id of device using this port (CRUD: CRUD)
        @type device_id: string
        @param device_owner: entity using this port (ex. dhcp agent,CRUD: CRUD)
        @type device_owner: string
        @param tenant_id: owner of the port (CRUD: CR)
        @type tenant_id: string
        @param security_groups: ids of any security groups associated with the
            port (CRUD: CRUD)
        @type security_groups: list(dict)
        @param resource_build_attempts: number of API retries
        @type resource_build_attempts: int
        @param raise_exception: flag to raise an exception if the Port was not
            created or to return None
        @type raise_exception: bool
        @param use_exact_name: flag if the exact name given should be used
        @type use_exact_name: bool
        @param poll_interval: sleep time interval between API retries
        @type poll_interval: int
        @param timeout: port create timeout for over limit retries
        @type timeout: int
        @param use_over_limit_retry: flag to enable/disable the port create
            over limits retries
        @type use_over_limit_retry: bool
        @return: NetworkingResponse object with api response and failure list
        @rtype: common.behaviors.NetworkingResponse
        """
        if not network_id:
            raise NetworkIDMissingException

        attrs_kwargs = dict(
            network_id=network_id, name=name,
            admin_state_up=admin_state_up, mac_address=mac_address,
            fixed_ips=fixed_ips, device_id=device_id,
            device_owner=device_owner, tenant_id=tenant_id,
            security_groups=security_groups)

        result = self._create_resource(
            resource=self.ports_resource,
            resource_build_attempts=resource_build_attempts,
            raise_exception=raise_exception, use_exact_name=use_exact_name,
            poll_interval=poll_interval, attrs_kwargs=attrs_kwargs,
            timeout=timeout, use_over_limit_retry=use_over_limit_retry)

        return result

    def update_port(self, port_id, name=None, admin_state_up=None,
                    fixed_ips=None, device_id=None, device_owner=None,
                    security_groups=None, resource_update_attempts=None,
                    raise_exception=False, poll_interval=None,
                    timeout=None, use_over_limit_retry=False):
        """
        @summary: Updates and verifies a specified Port
        @param port_id: The UUID for the port
        @type port_id: string
        @param name: human readable name for the port, may not be unique
            (CRUD: CRU)
        @type name: string
        @param admin_state_up: true or false (default true), the admin state
            of the port. If down, the port does not forward packets (CRUD: CRU)
        @type admin_state_up: bool
        @param fixed_ips: ip addresses for the port associating the port with
            the subnets where the IPs come from (CRUD: CRU)
        @type fixed_ips: list(dict)
        @param device_id: id of device using this port (CRUD: CRUD)
        @type device_id: string
        @param string device_owner: entity using this port (ex. dhcp agent,
            CRUD: CRUD)
        @type device_owner: string
        @param security_groups: ids of any security groups associated with the
            port (CRUD: CRUD)
        @type security_groups: list(dict)
        @param resource_update_attempts: number of API retries
        @type resource_update_attempts: int
        @param raise_exception: flag to raise an exception if the
            Port was not updated or to return None
        @type raise_exception: bool
        @param poll_interval: sleep time interval between API retries
        @type poll_interval: int
        @param timeout: port update timeout for over limit retries
        @type timeout: int
        @param use_over_limit_retry: flag to enable/disable the port update
            over limits retries
        @type use_over_limit_retry: bool
        @return: NetworkingResponse object with api response and failure list
        @rtype: common.behaviors.NetworkingResponse
        """
        attrs_kwargs = dict(
            name=name, admin_state_up=admin_state_up,
            fixed_ips=fixed_ips, device_id=device_id,
            device_owner=device_owner, security_groups=security_groups)

        result = self._update_resource(
            resource=self.ports_resource,
            resource_id=port_id,
            resource_update_attempts=resource_update_attempts,
            raise_exception=raise_exception, poll_interval=poll_interval,
            attrs_kwargs=attrs_kwargs, timeout=timeout,
            use_over_limit_retry=use_over_limit_retry)

        return result

    def get_port(self, port_id, resource_get_attempts=None,
                 raise_exception=False, poll_interval=None,
                 timeout=None, use_over_limit_retry=False):
        """
        @summary: Shows and verifies a specified port
        @param port_id: The UUID for the port
        @type port_id: string
        @param resource_get_attempts: number of API retries
        @type resource_get_attempts: int
        @param raise_exception: flag to raise an exception if the get
            Port was not as expected or to return None
        @type raise_exception: bool
        @param poll_interval: sleep time interval between API retries
        @type poll_interval: int
        @param timeout: port get timeout for over limit retries
        @type timeout: int
        @param use_over_limit_retry: flag to enable/disable the port get
            over limits retries
        @type use_over_limit_retry: bool
        @return: NetworkingResponse object with api response and failure list
        @rtype: common.behaviors.NetworkingResponse
        """
        result = self._get_resource(
            resource=self.ports_resource,
            resource_id=port_id,
            resource_get_attempts=resource_get_attempts,
            raise_exception=raise_exception, poll_interval=poll_interval,
            timeout=timeout, use_over_limit_retry=use_over_limit_retry)

        return result

    def list_ports(self, port_id=None, network_id=None, name=None, status=None,
                   admin_state_up=None, device_id=None, tenant_id=None,
                   device_owner=None, mac_address=None, limit=None,
                   marker=None, page_reverse=None, resource_list_attempts=None,
                   raise_exception=False, poll_interval=None, timeout=None,
                   use_over_limit_retry=False):
        """
        @summary: Lists ports and verifies the response is the expected
        @param port_id: The UUID for the port to filter by
        @type port_id: string
        @param network_id: network ID to filter by
        @type network_id: string
        @param name: port name to filter by
        @type name: string
        @param status: port status to filter by
        @type status: string
        @param admin_state_up: Admin state of the port to filter by
        @type admin_state_up: bool
        @param device_id: id of device to filter by
        @type device_id: string
        @param tenant_id: owner of the port to filter by
        @type tenant_id: string
        @param device_owner: device owner to filter by
        @type device_owner: string
        @param mac_address: mac address to filter by
        @type mac_address: string
        @param limit: page size
        @type limit: int
        @param marker: Id of the last item of the previous page
        @type marker: string
        @param page_reverse: direction of the page
        @type page_reverse: bool
        @param resource_list_attempts: number of API retries
        @type resource_list_attempts: int
        @param raise_exception: flag to raise an exception if the list
            Port was not as expected or to return None
        @type raise_exception: bool
        @param poll_interval: sleep time interval between API retries
        @type poll_interval: int
        @param timeout: port get timeout for over limit retries
        @type timeout: int
        @param use_over_limit_retry: flag to enable/disable the port update
            over limits retries
        @type use_over_limit_retry: bool
        @return: NetworkingResponse object with api response and failure list
        @rtype: common.behaviors.NetworkingResponse
        """
        params_kwargs = dict(
            port_id=port_id, network_id=network_id, name=name,
            status=status, admin_state_up=admin_state_up,
            device_id=device_id, tenant_id=tenant_id,
            device_owner=device_owner, mac_address=mac_address,
            limit=limit, marker=marker, page_reverse=page_reverse)

        result = self._list_resources(
            resource=self.ports_resource,
            resource_list_attempts=resource_list_attempts,
            raise_exception=raise_exception, poll_interval=poll_interval,
            params_kwargs=params_kwargs, timeout=timeout,
            use_over_limit_retry=use_over_limit_retry)

        return result

    def delete_port(self, port_id, resource_delete_attempts=None,
                    raise_exception=False, poll_interval=None,
                    timeout=None, use_over_limit_retry=False):
        """
        @summary: Deletes and verifies a specified port is deleted
        @param string port_id: The UUID for the port
        @type port_id: string
        @param resource_delete_attempts: number of API retries
        @type resource_delete_attempts: int
        @param raise_exception: flag to raise an exception if the deleted
            Port was not as expected or to return None
        @type raise_exception: bool
        @param poll_interval: sleep time interval between API retries
        @type poll_interval: int
        @param timeout: port delete timeout for over limit retries
        @type timeout: int
        @param use_over_limit_retry: flag to enable/disable the port delete
            over limits retries
        @type use_over_limit_retry: bool
        @return: NetworkingResponse object with api response and failure list
        @rtype: common.behaviors.NetworkingResponse
        """
        result = self._delete_resource(
            resource=self.ports_resource,
            resource_id=port_id,
            resource_delete_attempts=resource_delete_attempts,
            raise_exception=raise_exception, poll_interval=poll_interval,
            timeout=timeout, use_over_limit_retry=use_over_limit_retry)

        return result

    def delete_ports(self, port_list=None, name=None, tenant_id=None,
                     skip_delete=None):
        """
        @summary: deletes multiple ports
        @param port_list: list of port UUIDs
        @type port_list: list(str)
        @param name: port name to filter by, asterisk can be used at the end
            of the name to filter by name starts with, for ex. port_name*
            (name will be ignored if port_list given)
        @type name: string
        @param tenant_id: port tenant ID to filter by
        @type tenant_id: string (ignored if port_list given)
        @param skip_delete: list of network UUIDs that should skip deletion
        @type skip_delete: list
        @return: failed deletes list with port IDs and failures
        @rtype: list(dict)
        """
        result = self._delete_resources(
            resource_list=port_list, name=name,
            tenant_id=tenant_id, skip_delete=skip_delete,
            resource=self.ports_resource)
        return result

    def clean_port(self, port_id, timeout=None, poll_interval=None):
        """
        @summary: deletes a port within a time out
        @param string port_id: The UUID for the port
        @type port_id: string
        @param timeout: seconds to wait for the port to be deleted
        @type timeout: int
        @param poll_interval: sleep time interval between API delete/get calls
        @type poll_interval: int
        @return: None if delete was successful or the undeleted port_id
        @rtype: None or string
        """
        result = self._clean_resource(
            resource=self.ports_resource,
            resource_id=port_id,
            timeout=timeout, poll_interval=poll_interval)

        return result

    def clean_ports(self, ports_list, timeout=None, poll_interval=None):
        """
        @summary: deletes each port from a list calling clean_port
        @param ports_list: list of ports UUIDs
        @type ports_list: list(str)
        @param timeout: seconds to wait for the port to be deleted
        @type timeout: int
        @param poll_interval: sleep time interval between API delete/get calls
        @type poll_interval: int
        @return: list of undeleted ports UUIDs
        @rtype: list(str)
        """
        result = self._clean_resources(
            resource=self.ports_resource,
            resource_list=ports_list,
            timeout=timeout, poll_interval=poll_interval)

        return result
