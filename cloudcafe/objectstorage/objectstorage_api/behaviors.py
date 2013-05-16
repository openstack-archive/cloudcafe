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
from cloudcafe.objectstorage.objectstorage_api.config \
    import ObjectStorageAPIConfig
from cloudcafe.objectstorage.objectstorage_api.client \
    import ObjectStorageAPIClient


class ObjectStorageAPI_Behaviors(BaseBehavior):
    def __init__(self, client=None):
        self.client = client
        self.config = ObjectStorageAPIConfig()

    @behavior(ObjectStorageAPIClient)
    def create_container(self, name=None):
        response = self.client.create_container(name)
        if not response.ok:
            raise Exception('could not create container')
