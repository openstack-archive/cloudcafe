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

from cloudcafe.networking.lbaas.common.client import BaseLoadBalancersClient
from cloudcafe.networking.lbaas.lbaas_api.member.request import \
    CreateMember, UpdateMember
from cloudcafe.networking.lbaas.lbaas_api.member.response import \
    Member, Members


class MembersClient(BaseLoadBalancersClient):
    """
    Members Client

    @summary: Members are back-end server nodes that process client requests.

    """
    _MEMBERS_URL = "{base_url}/members"
    _MEMBER_URL = "{base_url}/members/{member_id}"

    def create_member(self, subnet_id, tenant_id, address, protocol_port,
                      weight=None, admin_state_up=None,
                      requestslib_kwargs=None):
        """Create Member
        @summary: Creates an instance of a member given the
            provided parameters
        @param subnet_id: Subnet in which to access this member.
        @type subnet_id: str
        @param tenant_id: Tenant to which this member is owned.
        @type tenant_id: str
        @param address: IP address of pool member.
        @type address: str
        @param protocol_port: TCP or UDP port
        @type protocol_port: int
        @param weight: Positive integer indicating relative portion of
            traffic from pool this member should receive (e.g., a member with
            a weight of 10 will receive five times as much traffic as a
            member with weight 2)
                Default: 1
        @type weight: int
        @param admin_state_up: If set to False, member will be created in an
            administratively down state
                Default: True
        @type admin_state_up: bool
        @return: Response Object containing response code and the
            member domain object
        @rtype: Requests.response
        """
        full_url = self._MEMBERS_URL.format(
            base_url=self.url)
        member_request_object = CreateMember(
            subnet_id=subnet_id, tenant_id=tenant_id, address=address,
            protocol_port=protocol_port, weight=weight,
            admin_state_up=admin_state_up)

        return self.request('POST', full_url,
                            response_entity_type=Member,
                            request_entity=member_request_object,
                            requestslib_kwargs=requestslib_kwargs)

    def list_members(self, requestslib_kwargs=None):
        """List Members
        @summary: List all members configured for the account.
        @rtype: Requests.response
        @note: This operation does not require a request body.
        """
        full_url = self._MEMBERS_URL.format(base_url=self.url)
        return self.request('GET', full_url,
                            response_entity_type=Members,
                            requestslib_kwargs=requestslib_kwargs)

    def update_member(self, member_id, weight=None, admin_state_up=None,
                      requestslib_kwargs=None):
        """Update Member
        @summary: Update the properties of a member given the
            provided parameters
        @param weight: Positive integer indicating relative portion of
            traffic from pool this member should receive (e.g., a member with
            a weight of 10 will receive five times as much traffic as a
            member with weight 2)
                Default: 1
        @type weight: int
        @param admin_state_up: If set to False, member will be created in an
            administratively down state
                Default: True
        @type admin_state_up: bool
        @return: Response Object containing response code.
        @rtype: Requests.response
        """
        update_member = UpdateMember(
            weight=weight, admin_state_up=admin_state_up)
        full_url = self._MEMBER_URL.format(
            base_url=self.url,
            member_id=member_id)
        return self.request('PUT', full_url,
                            request_entity=update_member,
                            response_entity_type=Member,
                            requestslib_kwargs=requestslib_kwargs)

    def get_member(self, member_id, requestslib_kwargs=None):
        """Get Member Details
        @summary: List details of the specified member.
        @param member_id: ID of the member to get details from.
        @type member_id: str
        @return: Response Object containing response code and the
            member domain object.
        @rtype: Requests.response
        @note: This operation does not require a request body.
        """
        full_url = self._MEMBER_URL.format(
            base_url=self.url,
            member_id=member_id)
        return self.request('GET', full_url,
                            response_entity_type=Member,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_member(self, member_id, requestslib_kwargs=None):
        """Delete Member
        @summary: Remove a member from the account.
        @param member_id: ID of the member to delete.
        @type member_id: str
        @return: Response Object containing response code.
        @rtype: Requests.response
        """
        full_url = self._MEMBER_URL.format(base_url=self.url,
                                           member_id=member_id)
        return self.request('DELETE', full_url,
                            requestslib_kwargs=requestslib_kwargs)
