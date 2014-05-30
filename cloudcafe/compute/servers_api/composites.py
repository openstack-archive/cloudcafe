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

from cloudcafe.compute.common.composites import BaseComputeComposite
from cloudcafe.compute.servers_api.client import ServersClient
from cloudcafe.compute.servers_api.config import ServersConfig
from cloudcafe.compute.servers_api.behaviors import ServerBehaviors


class ServersComposite(BaseComputeComposite):
    behavior_class = ServerBehaviors

    def __init__(self, auth_composite):
        super(ServersComposite, self).__init__(auth_composite)
        self.config = ServersConfig()
        self.client = ServersClient(**self.compute_auth_composite.client_args)
        self.behaviors = None
