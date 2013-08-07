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
from cloudcafe.identity.v2_0.tenants_api.models.responses.service \
    import Service, Services


class TestService(object):
    @classmethod
    def setup_class(cls):
        cls.name = "keystone-test"
        cls.type = "identity-test"
        cls.description = "Keystone Identity Service Test"
        cls.admin_ext = "OS-KSADM"
        cls.service_dict = {"name": cls.name,
                            "type": cls.type,
                            "description": cls.description}
        cls.expected_service = Service(name=cls.name,
                                       type_=cls.type,
                                       description=cls.description)
        cls.json_dict = json.dumps({
            "{0}:service".format(cls.admin_ext): cls.service_dict})
        cls.expected_services = Services(services=[cls.expected_service])
        cls.service_dict_list = [cls.service_dict]
        cls.services_json_dict = json.dumps({
            "{0}:services".format(cls.admin_ext): cls.service_dict_list})

    def test_dict_to_obj(self):
        assert self.expected_service == Service._dict_to_obj(self.service_dict)

    def test_json_to_obj(self):
        assert self.expected_service == Service._json_to_obj(self.json_dict)
        assert self.expected_services == Services._json_to_obj(
            self.services_json_dict)

    def test_obj_json(self):
        assert self.json_dict == self.expected_service._obj_to_json()

    def test_list_to_obj(self):
        self.expected_services == Services._list_to_obj(
            self.service_dict_list)
