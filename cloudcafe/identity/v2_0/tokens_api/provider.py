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

from cafe.engine.provider import BaseProvider
from cloudcafe.identity.v2_0.tokens_api.client import TokenAPI_Client
from cloudcafe.identity.v2_0.tokens_api.behaviors import TokenAPI_Behaviors
from cloudcafe.identity.v2_0.tokens_api.config import TokenAPI_Config


class TokenAPI_Provider(BaseProvider):

    def __init__(self):
        self.config = TokenAPI_Config()
        url = self.config.authentication_endpoint
        self.client = TokenAPI_Client(url, 'json', 'json')
        self.behaviors = TokenAPI_Behaviors(self.client)
