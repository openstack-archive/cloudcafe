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
from cafe.engine.behaviors import BaseBehavior, behavior
from cloudcafe.auth.config import UserConfig
from cloudcafe.extensions.saio_tempauth.v1_0.client import TempauthAPI_Client


class TempauthAPI_Behaviors(BaseBehavior):
    """
    Tempauth Behaviors for use with Swift All In One.
    """

    def __init__(self, client=None):
        self.client = client
        self.config = UserConfig()

    @behavior(TempauthAPI_Client)
    def get_access_data(self, username=None, password=None):

        username = username or self.config.username
        password = password or self.config.password

        access_data = None
        if username is not None and password is not None:
            access_data = self.client.authenticate(username, password)

        return access_data
