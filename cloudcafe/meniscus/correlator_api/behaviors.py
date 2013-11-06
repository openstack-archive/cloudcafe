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


class PublishingBehaviors(object):

    def __init__(self, publish_client, correlation_config,
                 storage_client, tenant_id=None, tenant_token=None):
        self.publish_client = publish_client
        self.correlation_config = correlation_config
        self.storage_client = storage_client
        self.tenant_id = tenant_id
        self.tenant_token = tenant_token

    def publish_from_config(self):
        resp = self.publish_client.publish(
            tenant_id=self.tenant_id,
            message_token=self.tenant_token,
            host=self.correlation_config.host,
            pname=self.correlation_config.pname,
            time=self.correlation_config.time,
            native=None)
        return resp

    def publish_overriding_config(self, tenant_id=None, tenant_token=None,
                                  host=None, pname=None, time=None,
                                  native=None):

        # Native could be an empty dict or list.
        if native is None:
            native = self.correlation_config.native

        resp = self.publish_client.publish(
            tenant_id=tenant_id or self.tenant_id,
            message_token=tenant_token or self.tenant_token,
            host=host or self.correlation_config.host,
            pname=pname or self.correlation_config.pname,
            time=time or self.correlation_config.time,
            native=native)
        return resp

    def get_messages_by_timestamp(self, timestamp, num_messages=10,
                                  tenant_id=None):
        if tenant_id is None:
            tenant_id = self.tenant_id

        resp = self.storage_client.find_term(name='time', value=timestamp,
                                             size=num_messages)

        # Copying all of the models into a fresh list
        return [model for model in resp]
