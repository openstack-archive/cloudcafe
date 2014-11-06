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
import time

from cloudcafe.common.tools.datagen import rand_name
from cloudcafe.networking.networks.common.behaviors \
    import NetworkingBaseBehaviors, NetworkingResponse
from cloudcafe.networking.networks.common.constants \
    import NeutronResponseCodes
from cloudcafe.networking.networks.common.exceptions \
    import NetworkIDMissingException, ResourceBuildException,\
    ResourceDeleteException, ResourceGetException, ResourceListException,\
    ResourceUpdateException


class PortsBehaviors(NetworkingBaseBehaviors):

    def __init__(self, ports_client, ports_config, networks_client,
                 networks_config, subnets_client, subnets_config):
        super(PortsBehaviors, self).__init__(
              networks_client, networks_config, subnets_client, subnets_config,
              ports_client, ports_config)
        self.config = ports_config
        self.client = ports_client

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
                    use_exact_name=False, poll_interval=None):
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
        @return: NetworkingResponse object with api response and failure list
        @rtype: common.behaviors.NetworkingResponse
        """
        if not network_id:
            raise NetworkIDMissingException

        if name is None:
            name = rand_name(self.config.starts_with_name)
        elif not use_exact_name:
            name = rand_name(name)

        poll_interval = poll_interval or self.config.api_poll_interval
        resource_build_attempts = (resource_build_attempts or
            self.config.api_retries)

        result = NetworkingResponse()
        err_msg = 'Port Create failure'
        for attempt in range(resource_build_attempts):
            self._log.debug('Attempt {0} of {1} building port {2}'.format(
                attempt + 1, resource_build_attempts, name))

            resp = self.client.create_port(
                network_id=network_id, name=name,
                admin_state_up=admin_state_up, mac_address=mac_address,
                fixed_ips=fixed_ips, device_id=device_id,
                device_owner=device_owner, tenant_id=tenant_id,
                security_groups=security_groups)

            resp_check = self.check_response(resp=resp,
                status_code=NeutronResponseCodes.CREATE_PORT, label=name,
                message=err_msg, network_id=network_id)

            result.response = resp
            if not resp_check:
                return result

            # Failures will be an empty list if the create was successful the
            # first time
            result.failures.append(resp_check)
            time.sleep(poll_interval)

        else:
            err_msg = (
                'Unable to create {0} port after {1} attempts: '
                '{2}').format(name, resource_build_attempts, result.failures)
            self._log.error(err_msg)
            if raise_exception:
                raise ResourceBuildException(err_msg)
            return result

    def update_port(self, port_id, name=None, admin_state_up=None,
                    fixed_ips=None, device_id=None, device_owner=None,
                    security_groups=None, resource_update_attempts=None,
                    raise_exception=False, poll_interval=None):
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
        @return: NetworkingResponse object with api response and failure list
        @rtype: common.behaviors.NetworkingResponse
        """
        poll_interval = poll_interval or self.config.api_poll_interval
        resource_update_attempts = (resource_update_attempts or
            self.config.api_retries)

        result = NetworkingResponse()
        err_msg = 'Port Update failure'
        for attempt in range(resource_update_attempts):
            self._log.debug('Attempt {0} of {1} updating port {2}'.format(
                attempt + 1, resource_update_attempts, port_id))

            resp = self.client.update_port(
                port_id=port_id, name=name, admin_state_up=admin_state_up,
                    fixed_ips=fixed_ips, device_id=device_id,
                    device_owner=device_owner, security_groups=security_groups)

            resp_check = self.check_response(resp=resp,
                status_code=NeutronResponseCodes.UPDATE_PORT,
                label=port_id, message=err_msg)

            result.response = resp
            if not resp_check:
                return result

            # Failures will be an empty list if the update was successful the
            # first time
            result.failures.append(resp_check)
            time.sleep(poll_interval)

        else:
            err_msg = (
                'Unable to update {0} port after {1} attempts: '
                '{2}').format(port_id, resource_update_attempts,
                              result.failures)
            self._log.error(err_msg)
            if raise_exception:
                raise ResourceUpdateException(err_msg)
            return result

    def get_port(self, port_id, resource_get_attempts=None,
                 raise_exception=False, poll_interval=None):
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
        @return: NetworkingResponse object with api response and failure list
        @rtype: common.behaviors.NetworkingResponse
        """
        poll_interval = poll_interval or self.config.api_poll_interval
        resource_get_attempts = (resource_get_attempts or
            self.config.api_retries)

        result = NetworkingResponse()
        err_msg = 'Port Get failure'
        for attempt in range(resource_get_attempts):
            self._log.debug('Attempt {0} of {1} getting network {2}'.format(
                attempt + 1, resource_get_attempts, port_id))

            resp = self.client.get_port(port_id=port_id)

            resp_check = self.check_response(resp=resp,
                status_code=NeutronResponseCodes.GET_PORT,
                label=port_id, message=err_msg)

            result.response = resp
            if not resp_check:
                return result

            # Failures will be an empty list if the get was successful the
            # first time
            result.failures.append(resp_check)
            time.sleep(poll_interval)

        else:
            err_msg = (
                'Unable to GET {0} port after {1} attempts: '
                '{2}').format(port_id, resource_get_attempts, result.failures)
            self._log.error(err_msg)
            if raise_exception:
                raise ResourceGetException(err_msg)
            return result

    def list_ports(self, port_id=None, network_id=None, name=None, status=None,
                   admin_state_up=None, device_id=None, tenant_id=None,
                   device_owner=None, mac_address=None, limit=None,
                   marker=None, page_reverse=None, resource_list_attempts=None,
                   raise_exception=False, poll_interval=None):
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
        @return: NetworkingResponse object with api response and failure list
        @rtype: common.behaviors.NetworkingResponse
        """
        poll_interval = poll_interval or self.config.api_poll_interval
        resource_list_attempts = (resource_list_attempts or
            self.config.api_retries)

        result = NetworkingResponse()
        err_msg = 'Port List failure'
        for attempt in range(resource_list_attempts):
            self._log.debug('Attempt {0} of {1} with port list'.format(
                attempt + 1, resource_list_attempts))

            resp = self.client.list_ports(
                port_id=port_id, network_id=network_id, name=name,
                status=status, admin_state_up=admin_state_up,
                device_id=device_id, tenant_id=tenant_id,
                device_owner=device_owner, mac_address=mac_address,
                limit=limit, marker=marker, page_reverse=page_reverse)

            resp_check = self.check_response(resp=resp,
                status_code=NeutronResponseCodes.LIST_PORTS,
                label='', message=err_msg)

            result.response = resp
            if not resp_check:
                return result

            # Failures will be an empty list if the list was successful the
            # first time
            result.failures.append(resp_check)
            time.sleep(poll_interval)

        else:
            err_msg = (
                'Unable to LIST ports after {0} attempts: '
                '{1}').format(resource_list_attempts, result.failures)
            self._log.error(err_msg)
            if raise_exception:
                raise ResourceListException(err_msg)
            return result

    def delete_port(self, port_id, resource_delete_attempts=None,
                    raise_exception=False, poll_interval=None):
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
        @return: NetworkingResponse object with api response and failure list
        @rtype: common.behaviors.NetworkingResponse
        """
        poll_interval = poll_interval or self.config.api_poll_interval
        resource_delete_attempts = (resource_delete_attempts or
            self.config.api_retries)

        result = NetworkingResponse()
        for attempt in range(resource_delete_attempts):
            self._log.debug('Attempt {0} of {1} deleting port {2}'.format(
                attempt + 1, resource_delete_attempts, port_id))

            resp = self.client.delete_port(port_id=port_id)
            result.response = resp

            # Delete response is without entity so resp_check can not be used
            if (resp.ok and
                resp.status_code == NeutronResponseCodes.DELETE_PORT):
                return result

            err_msg = ('{port} Port Delete failure, expected status '
                'code: {expected_status}. Response: {status} {reason} '
                '{content}').format(
                port=port_id,
                expected_status=NeutronResponseCodes.DELETE_PORT,
                status=resp.status_code, reason=resp.reason,
                content=resp.content)
            self._log.error(err_msg)
            result.failures.append(err_msg)
            time.sleep(poll_interval)

        else:
            err_msg = (
                'Unable to DELETE {0} port after {1} attempts: '
                '{2}').format(port_id, resource_delete_attempts,
                              result.failures)
            self._log.error(err_msg)
            if raise_exception:
                raise ResourceDeleteException(err_msg)
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
        timeout = timeout or self.config.resource_delete_timeout
        poll_interval = poll_interval or self.config.api_poll_interval
        endtime = time.time() + int(timeout)
        log_msg = 'Deleting {0} port within a {1}s timeout '.format(
            port_id, timeout)
        self._log.info(log_msg)
        resp = None
        while time.time() < endtime:
            try:
                self.client.delete_port(port_id=port_id)
                resp = self.client.get_port(port_id=port_id)
            except Exception as err:
                err_msg = ('Encountered an exception deleting a port with'
                    'the clean_network method. Exception: {0}').format(err)
                self._log.error(err_msg)

            if (resp is not None and
                resp.status_code == NeutronResponseCodes.NOT_FOUND):
                return None
            time.sleep(poll_interval)

        err_msg = 'Unable to delete {0} port within a {1}s timeout'.format(
            port_id, timeout)
        self._log.error(err_msg)
        return port_id

    def clean_ports(self, ports_list):
        """
        @summary: deletes each port from a list calling clean_port
        @param ports_list: list of ports UUIDs
        @type ports_list: list(str)
        @return: list of undeleted ports UUIDs
        @rtype: list(str)
        """
        log_msg = 'Deleting ports: {0}'.format(ports_list)
        self._log.info(log_msg)
        undeleted_ports = []
        for port in ports_list:
            result = self.clean_port(port_id=port)
            if result:
                undeleted_ports.append(result)
        if undeleted_ports:
            err_msg = 'Unable to delete ports: {0}'.format(
                undeleted_ports)
            self._log.error(err_msg)
        return undeleted_ports
