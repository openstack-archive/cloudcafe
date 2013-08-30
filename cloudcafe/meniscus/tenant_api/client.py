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

from cafe.engine.clients.rest import AutoMarshallingRestClient
from cloudcafe.meniscus.tenant_api.models.tenant import \
    Tenant, CreateTenant, ResetToken
from cloudcafe.meniscus.tenant_api.models.producer import \
    CreateProducer, UpdateProducer, AllProducers, Producer


class MeniscusClient(AutoMarshallingRestClient):

    def __init__(self, url, api_version, use_alternate=False,
                 serialize_format=None, deserialize_format=None):
        super(MeniscusClient, self).__init__(serialize_format,
                                             deserialize_format)
        self.url = url
        self.api_version = api_version
        self.use_alternate = use_alternate

    def _get_base_url(self):
        if not self.use_alternate:
            url = '{base}/{version}/tenant'.format(base=self.url,
                                                   version=self.api_version)
        else:
            url = '{base}/{version}'.format(base=self.url,
                                            version=self.api_version)
        return url


class TenantClient(MeniscusClient):

    def create_tenant(self, tenant_id):
        """
        @summary: Creates a tenant with the given id
        @param tenant_id:
        """
        url = self._get_base_url()
        resp = self.request('POST', url,
                            request_entity=CreateTenant(tenant_id))
        return resp

    def get_tenant(self, tenant_id):
        """
        @summary: Retrieves the version information from the API
        """
        url = '{base}/{tenant_id}'.format(base=self._get_base_url(),
                                          tenant_id=tenant_id)
        resp = self.request('GET', url, response_entity_type=Tenant)
        return resp

    def validate_token(self, tenant_id, msg_token, worker_id, worker_token):
        """
        HEAD /v1/{tenant_id}/token
        @summary: Checks to see if the token is valid
        """
        url = '{base}/{tenant_id}/token'.format(base=self._get_base_url(),
                                                tenant_id=tenant_id)
        headers = {
            'MESSAGE-TOKEN': msg_token,
            'WORKER-ID': worker_id,
            'WORKER-TOKEN': worker_token
        }
        return self.request('HEAD', url, headers=headers)

    def reset_token(self, tenant_id, invalidate_now):
        """
        POST /v1/{tenant_id}/token
        @summary: Should activate the reset token functionality.
        """
        url = '{base}/{tenant_id}/token'.format(base=self._get_base_url(),
                                                tenant_id=tenant_id)
        req_obj = ResetToken(invalidate_now)
        return self.request('POST', url, request_entity=req_obj)


class ProducerClient(MeniscusClient):
    def __init__(self, url, api_version, tenant_id, use_alternate=False,
                 serialize_format=None, deserialize_format=None):
        super(ProducerClient, self).__init__(url, api_version,
                                             use_alternate, serialize_format,
                                             deserialize_format)
        self.tenant_id = tenant_id

    def _generate_producer_url(self, producer_id):
        remote_url = '{base}/{tenant_id}/producers/{producer_id}'\
            .format(base=self._get_base_url(),
                    tenant_id=self.tenant_id,
                    producer_id=producer_id)
        return remote_url

    def create_producer(self, name=None, pattern=None,
                        durable=None, encrypted=None):
        """
        POST /{api_version}/{tenant_id}/producers
        @summary: Creates a new producer on a tenant
        """

        request_producer = CreateProducer(
            producer_name=name,
            producer_pattern=pattern,
            producer_durable=durable,
            producer_encrypted=encrypted)

        url = '{base}/{tenant_id}/producers'.format(
            base=self._get_base_url(),
            version=self.api_version,
            tenant_id=self.tenant_id)

        producer_request = self.request('POST', url,
                                        request_entity=request_producer)

        return producer_request

    def delete_producer(self, producer_id):
        """
        DELETE /{app_version}/{tenant_id}/producers/{producer_id}
        @summary: Removes a producer from a tenant
        """
        remote_url = self._generate_producer_url(producer_id)
        response = self.request('DELETE', remote_url)

        return response

    def update_producer(self, producer_id, name=None, pattern=None,
                        durable=None, encrypted=None):
        """
        PUT /{app_version}/{tenant_id}/producers/{producer_id}
        @summary: Updates a producer
        """
        producer_obj = UpdateProducer(producer_name=name,
                                      producer_pattern=pattern,
                                      producer_durable=durable,
                                      producer_encrypted=encrypted)
        remote_url = self._generate_producer_url(producer_id)
        response = self.request('PUT', remote_url, request_entity=producer_obj)
        return response

    def get_producer(self, producer_id):
        """
        GET /{app_version}/{tenant_id}/producers/{producer_id}
        @summary: Retrieves a Producer on a tenant
        """
        remote_url = self._generate_producer_url(producer_id)
        response = self.request('GET', remote_url,
                                response_entity_type=Producer)
        return response

    def get_all_producers(self):
        """
        GET /{app_version}/{tenant_id}/producers
        @summary: Retrieves all producers on a given tenants
        """
        remote_url = '{base}/{tenant_id}/producers'.format(
            base=self._get_base_url(),
            tenant_id=self.tenant_id)

        response = self.request('GET', remote_url,
                                response_entity_type=AllProducers)
        return response
