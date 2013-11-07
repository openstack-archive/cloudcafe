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
from cloudcafe.common.tools.datagen import random_int
from cloudcafe.meniscus.common.tools import RequestUtilities


class TenantBehaviors(object):

    def __init__(self, tenant_client, db_client, tenant_config, es_client):
        self.tenant_client = tenant_client
        self.db_client = db_client
        self.tenant_config = tenant_config
        self.es_client = es_client
        self.tenant_ids = []

    def remove_created_tenants(self):
        self.db_client.connect()
        self.db_client.auth()
        for tenant_id in self.tenant_ids:
            self.db_client.remove_tenant(tenant_id)
            self.es_client.wait_for_index(tenant_id)
            self.es_client.delete_index(tenant_id)
        self.db_client.disconnect()
        self.tenant_ids = []

    def create_tenant(self, tenant_id=None, use_alternate=False):
        """
        Helper function for creating a tenant on a fixture
        @param self:
        @return: Returns tuple with tenant_id and response object
        """
        if tenant_id is None:
            tenant_id = str(random_int(1, 100000))
        self.tenant_ids.append(tenant_id)

        if use_alternate:
            self.tenant_client.use_alternate = use_alternate

        resp = self.tenant_client.create_tenant(tenant_id)

        if use_alternate:
            self.tenant_client.use_alternate = False
        return tenant_id, resp


class ProducerBehaviors(TenantBehaviors):

    def __init__(self, tenant_client, producer_client, db_client,
                 tenant_config, es_client):
        super(ProducerBehaviors, self).__init__(tenant_client=tenant_client,
                                                db_client=db_client,
                                                tenant_config=tenant_config,
                                                es_client=es_client)
        self.producer_client = producer_client
        self.producers_created = []

    def create_producer_from_cfg(self, name=None, pattern=None, durable=None,
                                 encrypted=None):
        """
        @summary: Helper function to create a producer for fixtures. All
        parameters set to None will be loaded from configuration file.
        @return: Dictionary with request object, and producer id
        """

        resp = self.create_producer(
            name=name or self.tenant_config.producer_name,
            pattern=pattern or self.tenant_config.producer_pattern,
            durable=durable or self.tenant_config.producer_durable,
            encrypted=encrypted or self.tenant_config.producer_encrypted)

        return resp

    def create_producer(self, name=None, pattern=None, durable=None,
                        encrypted=None):
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
        assert response.status_code == 200

        if remove_from_array:
            self.producers_created.remove(producer_id)

        return response
