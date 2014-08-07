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

from cloudcafe.networking.lbaas.lbaas_api.clients.member.client import \
    MembersClient
from cloudcafe.networking.lbaas.lbaas_api.models.request.member import \
    CreateMember, UpdateMember
from cloudcafe.networking.lbaas.lbaas_api.models.response.member import \
    Member, Members


class MembersClientFixture(unittest.TestCase):
    """
    @summary: Member Client Tests
    """
    @classmethod
    def setUpClass(cls):
        super(MembersClientFixture, cls).setUpClass()

        cls.auth_token = "fake_auth_token"
        cls.url = "http://fake.url.endpoint"
        cls.member_id = "12345"
        cls.subnet_id = "SUBNET_ID"
        cls.tenant_id = "453105b9-1754-413f-aab1-55f1af620750"
        cls.address = "192.0.2.14"
        cls.protocol_port = 8080
        cls.weight = 7
        cls.admin_state_up = True

        cls.full_url_members = (
            MembersClient._MEMBERS_URL.format(
                base_url=cls.url))
        cls.full_url_member = (
            MembersClient._MEMBER_URL.format(
                base_url=cls.url,
                member_id=cls.member_id))

        cls.members_client = MembersClient(
            url=cls.url,
            auth_token=cls.auth_token,
            serialize_format=cls.SERIALIZE,
            deserialize_format=cls.DESERIALIZE)


class MembersClientTests(object):

    @mock.patch.object(MembersClient, 'request', autospec=True)
    def test_create_member(self, mock_request):

        create_member_kwargs = (
            {'subnet_id': self.subnet_id,
             'tenant_id': self.tenant_id,
             'address': self.address,
             'protocol_port': self.protocol_port,
             'weight': self.weight,
             'admin_state_up': self.admin_state_up})
        self.members_client.create_member(**create_member_kwargs)
        create_member_request = CreateMember(**create_member_kwargs)
        mock_request.assert_called_once_with(
            self.members_client,
            'POST',
            self.full_url_members,
            request_entity=create_member_request,
            response_entity_type=Member,
            requestslib_kwargs=None)

    @mock.patch.object(MembersClient, 'request', autospec=True)
    def test_list_member(self, mock_request):

        self.members_client.list_members()
        mock_request.assert_called_once_with(
            self.members_client,
            'GET',
            self.full_url_members,
            response_entity_type=Members,
            requestslib_kwargs=None)

    @mock.patch.object(MembersClient, 'request', autospec=True)
    def test_get_member(self, mock_request):

        self.members_client.get_member(member_id=self.member_id)
        mock_request.assert_called_once_with(
            self.members_client,
            'GET',
            self.full_url_member,
            response_entity_type=Member,
            requestslib_kwargs=None)

    @mock.patch.object(MembersClient, 'request', autospec=True)
    def test_update_member(self, mock_request):

        update_member_kwargs = (
            {'weight': self.weight,
             'admin_state_up': self.admin_state_up})
        self.members_client.update_member(member_id=self.member_id,
                                          **update_member_kwargs)
        update_member_request = UpdateMember(**update_member_kwargs)
        mock_request.assert_called_once_with(
            self.members_client,
            'PUT',
            self.full_url_member,
            request_entity=update_member_request,
            response_entity_type=Member,
            requestslib_kwargs=None)

    @mock.patch.object(MembersClient, 'request', autospec=True)
    def test_delete_member(self, mock_request):

        self.members_client.delete_member(member_id=self.member_id)
        mock_request.assert_called_once_with(self.members_client,
                                             'DELETE',
                                             self.full_url_member,
                                             requestslib_kwargs=None)


class MembersClientTestsXML(MembersClientFixture, MembersClientTests):
    SERIALIZE = 'xml'
    DESERIALIZE = 'xml'


class MembersClientTestsJSON(MembersClientFixture, MembersClientTests):
    SERIALIZE = 'json'
    DESERIALIZE = 'json'
