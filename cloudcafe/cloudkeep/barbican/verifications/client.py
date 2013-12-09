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
from cloudcafe.cloudkeep.barbican.client import BarbicanRestClient
from cloudcafe.cloudkeep.barbican.verifications.models.verification \
    import Verification, VerificationRequest, \
    VerificationRef, VerificationGroup


class VerificationsClient(BarbicanRestClient):

    def __init__(self, url, api_version, tenant_id, token=None,
                 serialize_format=None, deserialize_format=None):
        super(VerificationsClient, self).__init__(
            token=token, serialize_format=serialize_format,
            deserialize_format=deserialize_format)
        self.url = url
        self.api_version = api_version
        self.tenant_id = tenant_id

    def _get_base_url(self):
        return '{base}/{api_version}/{tenant_id}/verifications'.format(
            base=self.url,
            api_version=self.api_version,
            tenant_id=self.tenant_id)

    def _get_verification_url(self, verification_id):
        return '{base}/{verification_id}'.format(base=self._get_base_url(),
                                                 verification_id=
                                                 verification_id)

    def create_verification(self, resource_type=None, resource_ref=None,
                            resource_action=None, impersonation_allowed=False):
        """
        POST http://.../v1/{tenant_id}/verifications
        Creates a request to verify a resource
        """
        remote_url = self._get_base_url()
        req_obj = VerificationRequest(resource_type=resource_type,
                                      resource_ref=resource_ref,
                                      resource_action=resource_action,
                                      impersonation_allowed=
                                      impersonation_allowed)

        resp = self.request('POST', remote_url, request_entity=req_obj,
                            response_entity_type=VerificationRef)
        return resp

    def get_verification(self, verification_id=None, ref=None):
        """
        GET http://.../v1/{tenant_id}/verifications/{verification_uuid}
        Retrieves a verification
        """
        remote_url = ref or self._get_verification_url(verification_id)
        return self.request('GET', remote_url,
                            response_entity_type=Verification)

    def delete_verification(self, verification_id):
        """
        DELETE http://.../v1/{tenant_id}/verifications/{verification_uuid}
        Cancels a verification
        """
        return self.request('DELETE',
                            self._get_verification_url(verification_id))

    def get_verifications(self, limit=None, offset=None, ref=None):
        """
        GET http://.../v1/verifications?limit={limit}&offset={offset} or {ref}
        Gets a list of verifications
        """
        remote_url = ref or self._get_base_url()
        resp = self.request('GET', remote_url,
                            params={'limit': limit, 'offset': offset},
                            response_entity_type=VerificationGroup)
        return resp

