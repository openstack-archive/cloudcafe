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

from cafe.engine.behaviors import BaseBehavior


class NetworksAPIBehaviors(BaseBehavior):

    def __init__(self, networks_client, networks_config, subnets_client,
                 subnets_config, ports_client, ports_config):
        super(NetworksAPIBehaviors, self).__init__()
        self.config = networks_config
        self.client = networks_client
        self.subnets_client = subnets_client
        self.subnets_config = subnets_config
        self.ports_client = ports_client
        self.ports_config = ports_config
