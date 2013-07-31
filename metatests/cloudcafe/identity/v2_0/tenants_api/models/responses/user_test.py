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
from cloudcafe.identity.v2_0.tenants_api.models.responses.user \
    import User, Users


class TestUser(object):

    @classmethod
    def setup_class(cls):
        cls.user_id = "USER_ID"
        cls.user_name = "TEST_USER"
        cls.user_tenant_id = None
        cls.user_enabled = True
        cls.user_email = "user@test.com"
        cls.user_dict = {
            "id": cls.user_id,
            "name": cls.user_name,
            "tenantId": cls.user_tenant_id,
            "enabled": cls.user_enabled,
            "email": cls.user_email}

        cls.json_dict = {
            "name": cls.user_name,
            "tenantId": cls.user_tenant_id,
            "enabled": cls.user_enabled,
            "email": cls.user_email}

        cls.expected_user = User(id_=cls.user_id,
                                 name=cls.user_name,
                                 tenant_id=cls.user_tenant_id,
                                 enabled=cls.user_enabled,
                                 email=cls.user_email)
        cls.user_dict_list = [cls.user_dict]
        cls.expected_users = Users(users=[cls.expected_user])
        cls.expected_user_json = json.dumps({"user": cls.json_dict})
        cls.users_json = json.dumps({"users": cls.user_dict_list})

    def test_dict_to_obj(self):
        assert self.expected_user == User._dict_to_obj(self.user_dict)

    def test_list_to_obj(self):
        assert self.expected_users == Users._list_to_obj(self.user_dict_list)

    def test_json_to_obj(self):
        assert self.expected_user == User._json_to_obj(self.expected_user_json)
        assert self.expected_users == Users._json_to_obj(self.users_json)

    def test_obj_to_json(self):
        assert self.expected_user_json == self.expected_user._obj_to_json()
