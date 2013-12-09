"""
Copyright 2013 Rackspace

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
from httplib import BadStatusLine
from requests.exceptions import ConnectionError
from cloudcafe.cloudkeep.common.responses import CloudkeepResponse


class VerificationsBehavior(object):

    def __init__(self, verifications_client, config):
        super(VerificationsBehavior, self).__init__()
        self.verifications_client = verifications_client
        self.config = config
        self.created_verifications = []

    def create_and_check_verification(self, resource_type=None,
                                      resource_ref=None,
                                      resource_action=None,
                                      impersonation_allowed=False):
        """Creates verification, gets verification."""
        resp = self.create_verification_overriding_cfg(
            resource_type=resource_type, resource_ref=resource_ref,
            resource_action=resource_action,
            impersonation_allowed=impersonation_allowed)

        get_verification_resp = self.verifications_client.get_verification(
            verification_id=resp.id)
        behavior_response = CloudkeepResponse(resp=resp.create_resp,
                                              get_resp=get_verification_resp)
        return behavior_response

    def create_verification_from_config(self):
        """Creates verification from configuration."""

        resp = self.create_verification(
            resource_type=self.config.resource_type,
            resource_ref=self.config.resource_ref,
            resource_action=self.config.resource_action,
            impersonation_allowed=self.config.impersonation_allowed)
        return resp

    def create_verification_overriding_cfg(self, resource_type=None,
                                           resource_ref=None,
                                           resource_action=None,
                                           impersonation_allowed=False):
        """Creates verification using provided parameters or default
        configurations. Allows for testing individual parameters on creation.
        """
        if impersonation_allowed is None:
            imp_allowed = False
        else:
            imp_allowed = impersonation_allowed

        resp = self.create_verification(
            resource_type=resource_type or self.config.resource_type,
            resource_ref=
            resource_ref or self.config.resource_ref,
            resource_action=
            resource_action or self.config.resource_action,
            impersonation_allowed=imp_allowed)

        return resp

    def create_verification(self,
                            resource_type=None,
                            resource_ref=None,
                            resource_action=None,
                            impersonation_allowed=False):
        try:
            resp = self.verifications_client.create_verification(
                resource_type=resource_type,
                resource_ref=resource_ref,
                resource_action=resource_action,
                impersonation_allowed=impersonation_allowed)
        except ConnectionError as e:
            # Gracefully handling when Falcon doesn't properly handle our req
            if type(e.message.reason) is BadStatusLine:
                return {'status_code': 0}
            raise e

        behavior_response = CloudkeepResponse(resp=resp)
        verification_id = behavior_response.id
        if verification_id is not None:
            self.created_verifications.append(behavior_response.id)
        return behavior_response

    def delete_verification(self, verification_id):
        resp = self.verifications_client.delete_verification(verification_id)
        if verification_id in self.created_verifications:
            self.created_verifications.remove(verification_id)
        return resp

    def delete_all_verifications_in_db(self):
        verification_group = \
            self.verifications_client.get_verifications().entity
        found_ids = []
        found_ids.extend(verification_group.get_ids())

        while verification_group.next is not None:
            query = verification_group.get_next_query_data()
            verification_group = self.verifications_client.get_verifications(
                limit=query['limit'],
                offset=query['offset']).entity
            found_ids.extend(verification_group.get_ids())

        for verification_id in found_ids:
            self.delete_verification(verification_id)

    def delete_all_created_verifications(self):
        for verification_id in list(self.created_verifications):
            self.delete_verification(verification_id)
        self.created_verifications = []

    def remove_from_created_verifications(self, verification_id):
        if verification_id in self.created_verifications:
            self.created_verifications.remove(verification_id)

    def find_verification(self, verification_id):
        verification_group = \
            self.verifications_client.get_verifications().entity

        ids = verification_group.get_ids()
        while verification_id not in ids and \
                verification_group.next is not None:
            query = verification_group.get_next_query_data()
            verification_group = self.verifications_client.get_verifications(
                limit=query['limit'],
                offset=query['offset']).entity
            ids = verification_group.get_ids()

        for verification in verification_group.verifications:
            if verification.get_id() == verification_id:
                return verification
        else:
            return None
