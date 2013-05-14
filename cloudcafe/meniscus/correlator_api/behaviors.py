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

    def __init__(self, publish_client, correlation_config):
        self.publish_client = publish_client
        self.correlation_config = correlation_config

    def publish_from_config(self, tenant_id, tenant_token):
        return self.publish_message(tenant_id=tenant_id,
                                    tenant_token=tenant_token,
                                    host=self.correlation_config.host,
                                    pname=self.correlation_config.pname,
                                    time=self.correlation_config.time,
                                    native=self.correlation_config.native)

    def publish_message(self, tenant_id, tenant_token, host, pname, time,
                        native):
        return self.publish_client.publish(tenant_id=tenant_id,
                                           message_token=tenant_token,
                                           host=host,
                                           pname=pname,
                                           time=time,
                                           native=native)
