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

from unittest import TestCase
from cloudcafe.identity.v2_0.tenants_api.models.responses.role \
    import Role, Roles


class RoleTest(TestCase):
    def setUp(self):
        self.role_dict = {"id": "1", "name": "KeystoneServiceAdmin"}
        self.expected_role = Role(id_="1", name="KeystoneServiceAdmin")
        self.role_dict_list = [self.role_dict]
        self.expected_roles = Roles(roles=[self.expected_role])

    def test_dict_to_obj(self):
        assert self.expected_role == Role._dict_to_obj(self.role_dict)

    def test_list_to_obj(self):
        self.expected_roles == Roles._list_to_obj(self.role_dict_list)
