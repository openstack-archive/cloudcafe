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

import time

from cloudcafe.common.tools.datagen import rand_name
from cloudcafe.networking.networks.common.behaviors \
    import NetworkingBaseBehaviors
from cloudcafe.networking.networks.common.constants \
    import NeutronResponseCodes
from cloudcafe.networking.networks.common.exceptions \
    import ResourceBuildException, ResourceDeleteException,\
    ResourceGetException, ResourceListException, ResourceUpdateException


class NetworksBehaviors(NetworkingBaseBehaviors):

    def __init__(self, networks_client, networks_config, subnets_client,
                 subnets_config, ports_client, ports_config):
        super(NetworksBehaviors, self).__init__(
              networks_client, networks_config, subnets_client, subnets_config,
              ports_client, ports_config)
        self.config = networks_config
        self.client = networks_client

    def create_network(self, name=None, admin_state_up=None, shared=None,
                       tenant_id=None, resource_build_attempts=None,
                       raise_exception=True, use_exact_name=False):
        """
        @summary: Creates and verifies a Network is created as expected
        @param name: human readable name for the network, may not be unique
        @type name: string
        @param admin_state_up: true or false, the admin state of the network
        @type admin_state_up: bool
        @param shared: specifies if the network can be accessed by any tenant
        @type shared: bool
        @param tenant_id: owner of the network
        @type tenant_id: string
        @param resource_build_attempts: number of API retries
        @type resource_build_attempts: int
        @param raise_exception: flag to raise an exception if the
            Network was not created or to return None
        @type raise_exception: bool
        @param use_exact_name: flag if the exact name given should be used
        @type use_exact_name: bool
        @return: Network entity and the failure list if created successful, or
            None and the failure list if the raise_exception flag was False
        @rtype: tuple with Network or None and failure list (may be empty)
        """
        if name is None:
            name = rand_name(self.config.starts_with_name)
        elif not use_exact_name:
            name = rand_name(name)

        resource_build_attempts = (resource_build_attempts or
            self.config.resource_build_attempts)

        failures = []
        err_msg = 'Network Create failure'
        for attempt in range(resource_build_attempts):
            self._log.debug('Attempt {0} of {1} building network {2}'.format(
                attempt + 1, resource_build_attempts, name))

            resp = self.client.create_network(
                name=name, admin_state_up=admin_state_up, shared=shared,
                tenant_id=tenant_id)

            resp_check = self.check_response(resp=resp,
                status_code=NeutronResponseCodes.CREATE_NETWORK, label=name,
                message=err_msg)

            # Failures will be an empty list if the create was successful the
            # first time
            if not resp_check:
                return (resp.entity, failures)
            failures.append(resp_check)

        else:
            err_msg = (
                'Unable to create {0} network after {1} attempts: '
                '{2}').format(name, resource_build_attempts, failures)
            self._log.error(err_msg)
            if raise_exception:
                raise ResourceBuildException(err_msg)
            return (None, failures)

    def update_network(self, network_id, name=None, admin_state_up=None,
                       shared=None, tenant_id=None,
                       resource_update_attempts=None, raise_exception=False):
        """
        @summary: Updates and verifies a specified Network
        @param network_id: The UUID for the network
        @type network_id: string
        @param name: human readable name for the network, may not be unique.
            (CRUD: CRU)
        @type name: string
        @param admin_state_up: true or false, the admin state of the network.
            If down, the network does not forward packets.
            Usually set to True (CRUD: CRU)
        @type admin_state_up: bool
        @param shared: specifies if the network can be accessed by any tenant.
            Usually set to False (CRUD: CRU)
        @type shared: bool
        @param tenant_id: owner of the network. (CRUD: CR)
        @type tenant_id: string
        @param resource_update_attempts: number of API retries
        @type resource_update_attempts: int
        @param raise_exception: flag to raise an exception if the
            Network was not updated or to return None
        @type raise_exception: bool
        @return: Network entity and the failure list if updated successful, or
            None and the failure list if the raise_exception flag was False
        @rtype: tuple with Network or None and failure list (may be empty)
        """
        resource_update_attempts = (resource_update_attempts or
            self.config.resource_update_attempts)

        failures = []
        err_msg = 'Network Update failure'
        for attempt in range(resource_update_attempts):
            self._log.debug('Attempt {0} of {1} updating network {2}'.format(
                attempt + 1, resource_update_attempts, network_id))

            resp = self.client.update_network(
                network_id=network_id, name=name,
                admin_state_up=admin_state_up, shared=shared,
                tenant_id=tenant_id)

            resp_check = self.check_response(resp=resp,
                status_code=NeutronResponseCodes.UPDATE_NETWORK,
                label=network_id, message=err_msg)

            # Failures will be an empty list if the update was successful the
            # first time
            if not resp_check:
                return (resp.entity, failures)
            failures.append(resp_check)

        else:
            err_msg = (
                'Unable to update {0} network after {1} attempts: '
                '{2}').format(network_id, resource_update_attempts, failures)
            self._log.error(err_msg)
            if raise_exception:
                raise ResourceUpdateException(err_msg)
            return (None, failures)

    def get_network(self, network_id, resource_get_attempts=None,
                    raise_exception=False):
        """
        @summary: Shows and verifies a specified network
        @param network_id: The UUID for the network
        @type network_id: string
        @param resource_get_attempts: number of API retries
        @type resource_get_attempts: int
        @param raise_exception: flag to raise an exception if the get
            Network was not as expected or to return None
        @type raise_exception: bool
        @return: Network entity and the failure list if the get successful, or
            None and the failure list if the raise_exception flag was False
        @rtype: tuple with Network or None and failure list (may be empty)
        """
        resource_get_attempts = (resource_get_attempts or
            self.config.resource_get_attempts)

        failures = []
        err_msg = 'Network Get failure'
        for attempt in range(resource_get_attempts):
            self._log.debug('Attempt {0} of {1} getting network {2}'.format(
                attempt + 1, resource_get_attempts, network_id))

            resp = self.client.get_network(network_id=network_id)

            resp_check = self.check_response(resp=resp,
                status_code=NeutronResponseCodes.GET_NETWORK,
                label=network_id, message=err_msg)

            # Failures will be an empty list if the get was successful the
            # first time
            if not resp_check:
                return (resp.entity, failures)
            failures.append(resp_check)

        else:
            err_msg = (
                'Unable to GET {0} network after {1} attempts: '
                '{2}').format(network_id, resource_get_attempts, failures)
            self._log.error(err_msg)
            if raise_exception:
                raise ResourceGetException(err_msg)
            return (None, failures)

    def list_networks(self, network_id=None, name=None, status=None,
                      admin_state_up=None, shared=None, tenant_id=None,
                      limit=None, marker=None, page_reverse=None,
                      resource_list_attempts=None, raise_exception=False):
        """
        @summary: Lists networks and verifies the response is the expected
        @param network_id: network ID to filter by
        @type network_id: string
        @param name: network name to filter by
        @type name: string
        @param status: network status to filter by
        @type status: string
        @param admin_state_up: Admin state of the network to filter by
        @type admin_state_up: bool
        @param shared: If network is shared across tenants status to filter by
        @type shared: bool
        @param tenant_id: tenant ID network owner to filter by
        @type tenant_id: string
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
        @return: Network entity and the failure list if the list was successful
            or None and the failure list if the raise_exception flag was False
        @rtype: tuple with Network list or None and failure list (may be empty)
        """
        resource_list_attempts = (resource_list_attempts or
            self.config.resource_list_attempts)

        failures = []
        err_msg = 'Network List failure'
        for attempt in range(resource_list_attempts):
            self._log.debug('Attempt {0} of {1} with network list'.format(
                attempt + 1, resource_list_attempts))

            resp = self.client.list_networks(
                network_id=network_id, name=name, status=status,
                admin_state_up=admin_state_up, shared=shared,
                tenant_id=tenant_id, limit=limit, marker=marker,
                page_reverse=page_reverse)

            resp_check = self.check_response(resp=resp,
                status_code=NeutronResponseCodes.LIST_NETWORKS,
                label='', message=err_msg)

            # Failures will be an empty list if the list was successful the
            # first time
            if not resp_check:
                return (resp.entity, failures)
            failures.append(resp_check)

        else:
            err_msg = (
                'Unable to LIST networks after {0} attempts: '
                '{1}').format(resource_list_attempts, failures)
            self._log.error(err_msg)
            if raise_exception:
                raise ResourceListException(err_msg)
            return (None, failures)

    def delete_network(self, network_id, resource_delete_attempts=None,
                       raise_exception=False):
        """
        @summary: Deletes and verifies a specified network is deleted
        @param network_id: The UUID for the network
        @type network_id: string
        @param resource_delete_attempts: number of API retries
        @type resource_delete_attempts: int
        @param raise_exception: flag to raise an exception if the deleted
            Network was not as expected or to return None
        @type raise_exception: bool
        @return: True and the failure list if the delete was successful
            or None and the failure list if the raise_exception flag was False
        @rtype: tuple with True or None and failure list (may be empty)
        """
        resource_delete_attempts = (resource_delete_attempts or
            self.config.resource_delete_attempts)

        failures = []
        for attempt in range(resource_delete_attempts):
            self._log.debug('Attempt {0} of {1} deleting network {2}'.format(
                attempt + 1, resource_delete_attempts, network_id))

            resp = self.client.delete_network(network_id=network_id)

            # Delete response is without entity so resp_check can not be used
            if (resp.ok and
                resp.status_code == NeutronResponseCodes.DELETE_NETWORK):
                return (True, failures)
            err_msg = ('{network} Network Delete failure, expected status '
                'code: {expected_status}. Response: {status} {reason} '
                '{content}').format(
                network=network_id,
                expected_status=NeutronResponseCodes.DELETE_NETWORK,
                status=resp.status_code, reason=resp.reason,
                content=resp.content)
            self._log.error(err_msg)
            failures.append(err_msg)

        else:
            err_msg = (
                'Unable to DELETE {0} network after {1} attempts: '
                '{2}').format(network_id, resource_delete_attempts, failures)
            self._log.error(err_msg)
            if raise_exception:
                raise ResourceDeleteException(err_msg)
            return (None, failures)

    def clean_network(self, network_id, timeout=None, poll_interval=None):
        """
        @summary: deletes a network within a time out
        @param network_id: The UUID for the network
        @type network_id: string
        @param timeout: seconds to wait for the network to be deleted
        @type timeout: int
        @param poll_interval: sleep time interval between API delete/get calls
        @type poll_interval: int
        @return: None if delete was successful or the undeleted network_id
        @rtype: None or string
        """
        timeout = timeout or self.config.resource_delete_timeout
        poll_interval = poll_interval or self.config.api_poll_interval
        endtime = time.time() + int(timeout)
        log_msg = 'Deleting {0} network within a {1}s timeout '.format(
                    network_id, timeout)
        self._log.info(log_msg)
        while time.time() < endtime:
            try:
                self.client.delete_network(network_id=network_id)
                resp = self.client.get_network(network_id=network_id)
                if resp.status_code == NeutronResponseCodes.NOT_FOUND:
                    return None
            except Exception as err:
                err_msg = ('Encountered an exception deleting a network with'
                    'the clean_network method. Exception: {0}').format(err)
                self._log.error(err_msg)
            finally:
                time.sleep(poll_interval)
        err_msg = 'Unable to delete {0} network within a {1}s timeout'.format(
            network_id, timeout)
        self._log.error(err_msg)
        return network_id

    def clean_networks(self, networks_list):
        """
        @summary: deletes each network from a list calling clean_network
        @param network_list: list of network UUIDs
        @type network_list: list(str)
        @return: list of undeleted network UUIDs
        @rtype: list(str)
        """
        log_msg = 'Deleting networks: {0}'.format(networks_list)
        self._log.info(log_msg)
        undeleted_networks = []
        for network in networks_list:
            result = self.clean_network(network_id=network)
            if result:
                undeleted_networks.append(result)
        if undeleted_networks:
            err_msg = 'Unable to delete networks: {0}'.format(
                undeleted_networks)
            self._log.error(err_msg)
        return undeleted_networks
