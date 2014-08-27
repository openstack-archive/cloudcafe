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

from cloudcafe.networking.lbaas.common.behaviors import \
    BaseLoadBalancersBehaviors


class MemberBehaviors(BaseLoadBalancersBehaviors):

    OBJECT_MODEL = 'member'

    def __init__(self, members_client, config):
        super(MemberBehaviors, self).__init__(
            lbaas_client_type=members_client, config=config)

    def create_active_member(
            self, subnet_id, tenant_id, address, protocol_port,
            weight=None, admin_state_up=None):
        """
        @summary: Creates a member and waits for it to become active
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
        @return: Response object containing response and the member
                 domain object
        @rtype: requests.Response
        """
        kwargs = {'subnet_id': subnet_id, 'tenant_id': tenant_id,
                  'address': address, 'protocol_port': protocol_port,
                  'weight': weight, 'admin_state_up': admin_state_up}
        resp = self.create_active_lbaas_object(
            lbaas_model_type=self.OBJECT_MODEL,
            kwargs=kwargs)
        return resp

    def update_member_and_wait_for_active(self, weight=None,
                                          admin_state_up=None):
        """
        @summary: Updates a member and waits for it to become active
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
        @return: Response object containing response and the member
                 domain object
        @rtype: requests.Response
        """
        kwargs = {'weight': weight, 'admin_state_up': admin_state_up}
        resp = self.update_lbaas_object_and_wait_for_active(
            lbaas_model_type=self.OBJECT_MODEL,
            kwargs=kwargs)
        return resp

    def wait_for_member_status(self, member_id, desired_status,
                               interval_time=None, timeout=None):
        """
        @summary: Waits for a member to reach a desired status
        @param member_id: The id of the member
        @type member_id: String
        @param desired_status: The desired final status of the member
        @type desired_status: String
        @param interval_time: The amount of time in seconds to wait
            between polling
        @type interval_time: Integer
        @param interval_time: The amount of time in seconds to wait
            before aborting
        @type interval_time: Integer
        @return: Response object containing response and the member
            domain object
        @rtype: requests.Response
        """
        kwargs = {'member_id': member_id,
                  'desired_status': desired_status,
                  'interval_time': interval_time,
                  'timeout': timeout}
        resp = self.wait_for_lbaas_object_status(
            lbaas_model_type=self.OBJECT_MODEL, **kwargs)
        return resp
