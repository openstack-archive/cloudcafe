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
from cloudcafe.meniscus.tenant_api.models.tenant import Tenant, CreateTenant
from cloudcafe.meniscus.tenant_api.models.producer import \
    CreateProducer, UpdateProducer, AllProducers, Producer
from cloudcafe.meniscus.tenant_api.models.profile import \
    CreateProfile, UpdateProfile, AllProfiles, Profile
from cloudcafe.meniscus.tenant_api.models.host import \
    CreateHost, UpdateHost, AllHosts, Host


class TenantClient(AutoMarshallingRestClient):
    def __init__(self, url, api_version, serialize_format=None,
                 deserialize_format=None):
        """
        @param url: Base URL of meniscus api
        @type url: String
        """
        super(TenantClient, self).__init__(serialize_format,
                                           deserialize_format)
        self.url = url
        self.api_version = api_version

    def create_tenant(self, tenant_id):
        """
        @summary: Creates a tenant with the given id
        @param tenant_id:
        """
        url = '{base}/{version}'.format(base=self.url,
                                        version=self.api_version)

        resp = self.request('POST', url,
                            request_entity=CreateTenant(tenant_id))
        return resp

    def get_tenant(self, tenant_id):
        """
        @summary: Retrieves the version information from the API
        """
        url = '{base}/{version}/{tenant_id}'.format(
            base=self.url,
            version=self.api_version,
            tenant_id=tenant_id)

        resp = self.request('GET', url, response_entity_type=Tenant)
        return resp


class ProducerClient(AutoMarshallingRestClient):
    def __init__(self, url, api_version, tenant_id, serialize_format=None,
                 deserialize_format=None):
        super(ProducerClient, self).__init__(serialize_format,
                                             deserialize_format)
        self.url = url
        self.api_version = api_version
        self.tenant_id = tenant_id

    def _generate_producer_url(self, producer_id):
        remote_url = '{base}/{version}/{tenant_id}/producers/{producer_id}'\
            .format(base=self.url,
                    version=self.api_version,
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

        url = '{base}/{version}/{tenant_id}/producers'.format(
            base=self.url,
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
        remote_url = '{base}/{version}/{tenant_id}/producers'.format(
            base=self.url,
            version=self.api_version,
            tenant_id=self.tenant_id)

        response = self.request('GET', remote_url,
                                response_entity_type=AllProducers)
        return response


class ProfileClient(AutoMarshallingRestClient):

    def __init__(self, url, api_version, tenant_id, producer_id,
                 serialize_format=None, deserialize_format=None):
        super(ProfileClient, self).__init__(serialize_format,
                                            deserialize_format)
        self.url = url
        self.api_version = api_version
        self.tenant_id = tenant_id
        self.producer_id = producer_id

    def _generate_profile_url(self, profile_id):
        remote_url = '{base}/{version}/{tenant_id}/profiles/{profile_id}'\
            .format(base=self.url,
                    version=self.api_version,
                    tenant_id=self.tenant_id,
                    profile_id=profile_id)
        return remote_url

    def create_profile(self, name=None, producer_ids=None):
        """
        POST /{app_version}/{tenant_id}/profiles
        @summary: Creates a profile on a tenant
        """

        request_profile = CreateProfile(name=name,
                                        producer_ids=producer_ids)
        url = '{base}/{version}/{tenant_id}/profiles'.format(
            base=self.url,
            version=self.api_version,
            tenant_id=self.tenant_id)

        profile_request = self.post(url, request_entity=request_profile)
        return profile_request

    def get_profile(self, profile_id):
        """
        GET /{app_version}/{tenant_id}/profiles/{profile_id}
        @summary: Retrieves a profile from a tenant
        """
        remote_url = self._generate_profile_url(profile_id)
        response = self.request('GET', remote_url,
                                response_entity_type=Profile)
        return response

    def get_all_profiles(self):
        """
        GET /{app_version}/{tenant_id}/profiles
        @summary: Retrieves all profiles from a tenant
        """
        remote_url = '{base}/{version}/{tenant_id}/profiles'.format(
            base=self.url,
            version=self.api_version,
            tenant_id=self.tenant_id)

        response = self.request('GET', remote_url,
                                response_entity_type=AllProfiles)
        return response

    def delete_profile(self, profile_id):
        """
        DELETE /{app_version}/{tenant_id}/profiles/{profile_id}
        @summary: Removes a profile from a tenant
        """
        remote_url = self._generate_profile_url(profile_id)
        response = self.request('DELETE', remote_url)

        return response

    def update_profile(self, id, name=None, producer_ids=None):
        """
        PUT /{app_version}/{tenant_id}/profiles/{profile_id}
        @summary: Updates a profile on a tenant
        """
        profile_obj = UpdateProfile(name=name, producer_ids=producer_ids)

        remote_url = self._generate_profile_url(id)
        response = self.request('PUT', remote_url, request_entity=profile_obj)
        return response


class HostClient(AutoMarshallingRestClient):

    def __init__(self, url, api_version, tenant_id, profile_id,
                 serialize_format=None, deserialize_format=None):
        super(HostClient, self).__init__(serialize_format,
                                         deserialize_format)
        self.url = url
        self.api_version = api_version
        self.tenant_id = tenant_id
        self.profile_id = profile_id

    def _generate_host_url(self, host_id):
        remote_url = '{base}/{version}/{tenant_id}/hosts/{host_id}'.format(
            base=self.url,
            version=self.api_version,
            tenant_id=self.tenant_id,
            host_id=host_id)
        return remote_url

    def create_host(self, hostname, ip_v4, ip_v6, profile_id):
        """
        POST /{app_version}/{tenant_id}/hosts
        @summary: Creates a new host on a tenant
        """
        remote_url = '{base}/{version}/{tenant_id}/hosts'.format(
            base=self.url,
            version=self.api_version,
            tenant_id=self.tenant_id)

        host = CreateHost(hostname, profile_id, ip_v4, ip_v6)
        response = self.request('POST', remote_url, request_entity=host)

        return response

    def get_host(self, host_id):
        """
        GET /{app_version}/{tenant_id}/hosts/{host_id}
        @summary: Retrieves a host from a tenant
        """
        remote_url = self._generate_host_url(host_id)
        response = self.request('GET', remote_url,
                                response_entity_type=Host)
        return response

    def get_all_hosts(self):
        """
        GET /{app_version}/{tenant_id}/hosts
        @summary: Retrieves all hosts from a tenant
        """
        remote_url = '{base}/{version}/{tenant_id}/hosts'.format(
            base=self.url,
            version=self.api_version,
            tenant_id=self.tenant_id)

        response = self.request('GET', remote_url,
                                response_entity_type=AllHosts)
        return response

    def update_host(self, host_id, hostname=None, ip_v4=None, ip_v6=None,
                    profile_id=None):
        """
        PUT /{app_version}/{tenant_id}/hosts/{host_id}
        @summary: Update a single host on a tenant
        """
        remote_url = self._generate_host_url(host_id)
        host = UpdateHost(hostname, profile_id, ip_v4, ip_v6)

        response = self.request('PUT', remote_url, request_entity=host)
        return response

    def delete_host(self, host_id):
        """
        DELETE /{app_version}/{tenant_id}/hosts/{host_id}
        @summary: Removes a host from a tenant
        """
        remote_url = self._generate_host_url(host_id)
        response = self.request('DELETE', remote_url)

        return response
