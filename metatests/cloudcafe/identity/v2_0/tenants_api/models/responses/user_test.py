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
import json

from unittest import TestCase
from cloudcafe.identity.v2_0.tenants_api.models.responses.user \
    import User, Users


class UserTest(TestCase):
    def setUp(self):
        self.user_id = "USER_ID"
        self.user_name = "TEST_USER"
        self.user_tenant_id = None
        self.user_enabled = True
        self.user_email = "user@test.com"
        self.user_dict = {
            "name": self.user_name,
            "id": self.user_id,
            "tenantId": self.user_tenant_id,
            "enabled": self.user_enabled,
            "email": self.user_email}

        self.expected_user = User(id_=self.user_id,
                                  name=self.user_name,
                                  tenant_id=self.user_tenant_id,
                                  enabled=self.user_enabled,
                                  email=self.user_email)
        self.user_dict_list = [self.user_dict]
        self.expected_users = Users(users=[self.expected_user])
        self.serialized_str = json.dumps({"user": self.user_dict})
        self.expected_json = json.loads(self.serialized_str)

    def test_dict_to_obj(self):
        assert self.expected_user == User._dict_to_obj(self.user_dict)

    def test_list_to_obj(self):
        self.expected_users == Users._list_to_obj(self.user_dict_list)

    def test_json_to_obj(self):
        self.expected_user == User._json_to_obj(self.serialized_str)

    def test_obj_to_json(self):
        self.expected_json == self.expected_user._obj_to_json()
