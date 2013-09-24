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
from cafe.engine.models.base import BaseModel


class AuthData(BaseModel):
    """
    Tempauth data model for use with Swift All In One.
    """

    def __init__(self, storage_url, auth_token, storage_token):
        super(AuthData, self).__init__()
        self.storage_url = storage_url
        self.auth_token = auth_token
        self.storage_token = storage_token
