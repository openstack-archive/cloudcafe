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

from cloudcafe.networking.networks.common.behaviors \
    import NetworkingBaseBehaviors
from cloudcafe.networking.networks.common.constants \
    import NeutronResource, NeutronResponseCodes


class NetworksBehaviors(NetworkingBaseBehaviors):

    def __init__(self, networks_client, networks_config):
        super(NetworksBehaviors, self).__init__()
        self.config = networks_config
        self.client = networks_client
        self.response_codes = NeutronResponseCodes
        self.networks_resource = NeutronResource(NeutronResource.NETWORK)

    def create_network(self, name=None, admin_state_up=None, shared=None,
                       tenant_id=None, resource_build_attempts=None,
                       raise_exception=True, use_exact_name=False,
                       poll_interval=None):
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
        @param poll_interval: sleep time interval between API retries
        @type poll_interval: int
        @return: NetworkingResponse object with api response and failure list
        @rtype: common.behaviors.NetworkingResponse
        """
        attrs_kwargs = dict(name=name, admin_state_up=admin_state_up,
                            shared=shared, tenant_id=tenant_id)

        result = self._create_resource(
            resource=self.networks_resource,
            resource_build_attempts=resource_build_attempts,
            raise_exception=raise_exception, use_exact_name=use_exact_name,
            poll_interval=poll_interval, attrs_kwargs=attrs_kwargs)

        return result

    def update_network(self, network_id, name=None, admin_state_up=None,
                       shared=None, tenant_id=None,
                       resource_update_attempts=None, raise_exception=False,
                       poll_interval=None):
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
        @param poll_interval: sleep time interval between API retries
        @type poll_interval: int
        @return: NetworkingResponse object with api response and failure list
        @rtype: common.behaviors.NetworkingResponse
        """
        attrs_kwargs = dict(name=name, admin_state_up=admin_state_up,
                            shared=shared, tenant_id=tenant_id)

        result = self._update_resource(
            resource=self.networks_resource,
            resource_id=network_id,
            resource_update_attempts=resource_update_attempts,
            raise_exception=raise_exception, poll_interval=poll_interval,
            attrs_kwargs=attrs_kwargs)

        return result

    def get_network(self, network_id, resource_get_attempts=None,
                    raise_exception=False, poll_interval=None):
        """
        @summary: Shows and verifies a specified network
        @param network_id: The UUID for the network
        @type network_id: string
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
            resource=self.networks_resource,
            resource_id=network_id,
            resource_get_attempts=resource_get_attempts,
            raise_exception=raise_exception, poll_interval=poll_interval)

        return result

    def list_networks(self, network_id=None, name=None, status=None,
                      admin_state_up=None, shared=None, tenant_id=None,
                      limit=None, marker=None, page_reverse=None,
                      resource_list_attempts=None, raise_exception=False,
                      poll_interval=None):
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
        @param poll_interval: sleep time interval between API retries
        @type poll_interval: int
        @return: NetworkingResponse object with api response and failure list
        @rtype: common.behaviors.NetworkingResponse
        """
        params_kwargs = dict(network_id=network_id, name=name, status=status,
                             admin_state_up=admin_state_up, shared=shared,
                             tenant_id=tenant_id, limit=limit, marker=marker,
                             page_reverse=page_reverse)

        result = self._list_resources(
            resource=self.networks_resource,
            resource_list_attempts=resource_list_attempts,
            raise_exception=raise_exception, poll_interval=poll_interval,
            params_kwargs=params_kwargs)

        return result

    def delete_network(self, network_id, resource_delete_attempts=None,
                       raise_exception=False, poll_interval=None):
        """
        @summary: Deletes and verifies a specified network is deleted
        @param network_id: The UUID for the network
        @type network_id: string
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
            resource=self.networks_resource,
            resource_id=network_id,
            resource_delete_attempts=resource_delete_attempts,
            raise_exception=raise_exception, poll_interval=poll_interval)

        return result

    def delete_networks(self, network_list=None, name=None, tenant_id=None,
                        skip_delete=None):
        """
        @summary: deletes multiple networks
        @param network_list: list of network UUIDs
        @type network_list: list(str)
        @param name: network name to filter by, asterisk can be used at the end
            of the name to filter by name starts with, for ex. network_name*
            (name will be ignored if network_list given)
        @type name: string
        @param tenant_id: network tenant ID to filter by
        @type tenant_id: string (ignored if network_list given)
        @param skip_delete: list of network UUIDs that should skip deletion
        @type skip_delete: list
        @return: failed deletes list with network IDs and failures
        @rtype: list(dict)
        """
        result = self._delete_resources(
            resource_list=network_list, name=name,
            tenant_id=tenant_id, skip_delete=skip_delete,
            resource=self.networks_resource)

        return result

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
        result = self._clean_resource(
            resource=self.networks_resource,
            resource_id=network_id,
            timeout=timeout, poll_interval=poll_interval)

        return result

    def clean_networks(self, networks_list, timeout=None, poll_interval=None):
        """
        @summary: deletes each network from a list calling clean_network
        @param networks_list: list of network UUIDs
        @type networks_list: list(str)
        @param timeout: seconds to wait for the network to be deleted
        @type timeout: int
        @param poll_interval: sleep time interval between API delete/get calls
        @type poll_interval: int
        @return: list of undeleted networks UUIDs
        @rtype: list(str)
        """
        result = self._clean_resources(
            resource=self.networks_resource,
            resource_list=networks_list,
            timeout=timeout, poll_interval=poll_interval)

        return result
