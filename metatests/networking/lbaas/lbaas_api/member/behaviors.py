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

import mock
import unittest

from cloudcafe.networking.lbaas.lbaas_api.member.behaviors \
    import MemberBehaviors
from cloudcafe.networking.lbaas.lbaas_api.member.client \
    import MembersClient


class MemberBehaviorsFixture(unittest.TestCase):
    """
    @summary: Health Monitor Behaviors Tests
    """
    @classmethod
    def setUpClass(cls):
        super(MemberBehaviorsFixture, cls).setUpClass()

        cls.auth_token = "fake_auth_token"
        cls.url = "http://fake.url.endpoint"
        cls.member_id = "12345"
        cls.subnet_id = "SUBNET_ID"
        cls.tenant_id = "453105b9-1754-413f-aab1-55f1af620750"
        cls.address = "192.0.2.14"
        cls.protocol_port = 8080
        cls.weight = 7
        cls.admin_state_up = True

        cls.desired_status = "ACTIVE"
        cls.interval_time = 20
        cls.timeout = 120

        cls.members_client = MembersClient(
            url=cls.url,
            auth_token=cls.auth_token,
            serialize_format=cls.SERIALIZE,
            deserialize_format=cls.DESERIALIZE)

        cls.member_behaviors = MemberBehaviors(
            members_client=cls.members_client, config=None)


class MemberBehaviorsTests(object):

    @mock.patch.object(MemberBehaviors, 'create_active_member',
                       autospec=True)
    def test_create_active_member(self, mock_request):
        create_active_member_kwargs = (
            {'subnet_id': self.subnet_id,
             'tenant_id': self.tenant_id,
             'address': self.address,
             'protocol_port': self.protocol_port,
             'weight': self.weight,
             'admin_state_up': self.admin_state_up})
        self.member_behaviors.create_active_member(
            **create_active_member_kwargs)
        mock_request.assert_called_once_with(
            self.member_behaviors,
            **create_active_member_kwargs)

    @mock.patch.object(MemberBehaviors, 'update_member_and_wait_for_active',
                       autospec=True)
    def test_update_member_and_wait_for_active(self, mock_request):
        update_member_and_wait_for_active_kwargs = (
            {'weight': self.weight,
             'admin_state_up': self.admin_state_up})
        self.member_behaviors.update_member_and_wait_for_active(
            **update_member_and_wait_for_active_kwargs)
        mock_request.assert_called_once_with(
            self.member_behaviors,
            **update_member_and_wait_for_active_kwargs)

    @mock.patch.object(MemberBehaviors, 'wait_for_member_status',
                       autospec=True)
    def test_wait_for_member_status(self, mock_request):
        wait_for_member_status_kwargs = (
            {'member_id': self.member_id,
             'desired_status': self.desired_status,
             'interval_time': self.interval_time,
             'timeout': self.timeout})
        self.member_behaviors.wait_for_member_status(
            **wait_for_member_status_kwargs)
        mock_request.assert_called_once_with(
            self.member_behaviors,
            **wait_for_member_status_kwargs)


class MembersClientTestsXML(MemberBehaviorsFixture,
                            MemberBehaviorsTests):
    SERIALIZE = 'xml'
    DESERIALIZE = 'xml'


class MembersClientTestsJSON(MemberBehaviorsFixture,
                             MemberBehaviorsTests):
    SERIALIZE = 'json'
    DESERIALIZE = 'json'
