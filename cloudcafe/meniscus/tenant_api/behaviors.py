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
from cloudcafe.compute.common.datagen import random_int
from cloudcafe.meniscus.common.tools import RequestUtilities


class TenantBehaviors(object):

    def __init__(self, tenant_client, tenant_config):
        self.tenant_client = tenant_client
        self.tenant_config = tenant_config

    def create_tenant(self):
        """
        Helper function for creating a tenant on a fixture
        @param self:
        @return: Returns tuple with tenant_id and response object
        """
        tenant_id = random_int(1, 100000)
        resp = self.tenant_client.create_tenant(tenant_id)
        return str(tenant_id), resp


class ProducerBehaviors(TenantBehaviors):

    def __init__(self, tenant_client, producer_client, tenant_config):
        super(ProducerBehaviors, self).__init__(tenant_client=tenant_client,
                                                tenant_config=tenant_config)
        self.producer_client = producer_client
        self.producers_created = []

    def create_producer(self, name=None, pattern=None, durable=None,
                        encrypted=None):
        """
        @summary: Helper function to create a producer for fixtures. All
        parameters set to None will be loaded from configuration file.
        @return: Dictionary with request object, and producer id
        """
        if name is None:
            name = self.tenant_config.producer_name
        if pattern is None:
            pattern = self.tenant_config.producer_pattern
        if durable is None:
            durable = self.tenant_config.producer_durable
        if encrypted is None:
            encrypted = self.tenant_config.producer_encrypted

        req = self.producer_client.create_producer(
            name=name, pattern=pattern, durable=durable, encrypted=encrypted)

        producer_id = RequestUtilities.get_id(req)

        self.producers_created.append(producer_id)

        return {
            'request': req,
            'producer_id': producer_id
        }

    def delete_producer(self, producer_id, remove_from_array=True):
        response = self.producer_client.delete_producer(producer_id)
        if remove_from_array:
            self.producers_created.remove(producer_id)

        return response


class ProfileBehaviors(ProducerBehaviors):

    def __init__(self, tenant_client, producer_client, profile_client,
                 tenant_config):
        super(ProfileBehaviors, self).__init__(
            tenant_client=tenant_client,
            producer_client=producer_client,
            tenant_config=tenant_config)
        self.profile_client = profile_client
        self.profiles_created = []

    def create_new_profile(self, name=None, producer_ids=None):

        if name is None:
            name = self.tenant_config.profile_name

        profile_req = self.profile_client.create_profile(
            name=name, producer_ids=producer_ids)
        profile_id = RequestUtilities.get_id(profile_req)

        self.profiles_created.append(profile_id)

        return {
            'request': profile_req,
            'profile_id': profile_id
        }

    def delete_profile(self, profile_id, remove_from_array=True):
        response = self.profile_client.delete_profile(profile_id)
        if remove_from_array:
            self.profiles_created.remove(profile_id)

        return response


class HostBehaviors(ProfileBehaviors):

    def __init__(self, tenant_client, producer_client, profile_client,
                 host_client, tenant_config):
        super(HostBehaviors, self).__init__(
            tenant_client=tenant_client,
            producer_client=producer_client,
            profile_client=profile_client,
            tenant_config=tenant_config)
        self.host_client = host_client
        self.hosts_created = []

    def delete_host(self, host_id, remove_from_array=True):
        response = self.host_client.delete_host(host_id)

        if remove_from_array:
            self.hosts_created.remove(host_id)

        return response

    def create_new_host(self, hostname=None, ip_v4=None, ip_v6=None,
                        profile_id=None):
        if hostname is None:
            hostname = self.tenant_config.hostname

        host_req = self.host_client.create_host(
            hostname=hostname, ip_v4=ip_v4, ip_v6=ip_v6,
            profile_id=profile_id)

        host_id = RequestUtilities.get_id(host_req)
        self.hosts_created.append(host_id)

        return {
            'request': host_req,
            'host_id': host_id
        }
