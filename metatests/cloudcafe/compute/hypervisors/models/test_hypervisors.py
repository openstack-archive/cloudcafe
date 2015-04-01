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

import unittest
from cloudcafe.compute.hypervisors_api.model.hypervisor import Hypervisors


class HypervisorsDomainTest(object):

    def test_hypervisor_attr(self):
        self.assertEqual(self.hypervisors[0].id_, '1')
        self.assertEqual(self.hypervisors[0].hypervisor_hostname,
                         "hypervisor_test")
        self.assertEqual(self.hypervisors[0].vcpus_used, '2')
        self.assertEqual(self.hypervisors[0].hypervisor_type, 'xen')
        self.assertEqual(self.hypervisors[0].local_gb_used, '21')
        self.assertEqual(self.hypervisors[0].memory_mb_used, '4608')
        self.assertEqual(self.hypervisors[0].memory_mb, '12285')
        self.assertEqual(self.hypervisors[0].current_workload, '0')
        self.assertEqual(self.hypervisors[0].vcpus, '0')
        self.assertEqual(self.hypervisors[0].cpu_info, '2')
        self.assertEqual(self.hypervisors[0].running_vms, '2')
        self.assertEqual(self.hypervisors[0].free_disk_gb, '888')
        self.assertEqual(self.hypervisors[0].hypervisor_version, '6000000')
        self.assertEqual(self.hypervisors[0].disk_available_least, 'None')
        self.assertEqual(self.hypervisors[0].local_gb, '909')
        self.assertEqual(self.hypervisors[0].free_ram_mb, '7677')
        self.assertEqual(self.hypervisors[0].service.host, "parentcell")
        self.assertEqual(self.hypervisors[0].service.id_, '7')


class HypervisorsDomainJSONTest(unittest.TestCase, HypervisorsDomainTest):

    @classmethod
    def setUp(cls):
        cls.hypervisor_json = """
        {
            "hypervisors":[
                {
                "service":
                {
                    "host":"parentcell",
                    "id":"7"
                },
                "vcpus_used":"2",
                "hypervisor_type":"xen",
                "local_gb_used":"21",
                "hypervisor_hostname":"hypervisor_test",
                "memory_mb_used":"4608",
                "memory_mb":"12285",
                "current_workload":"0",
                "vcpus":"0",
                "cpu_info": "2",
                "running_vms":"2",
                "free_disk_gb":"888",
                "hypervisor_version":"6000000",
                "disk_available_least":"None",
                "local_gb":"909",
                "free_ram_mb":"7677",
                "id":"1"
                }
            ]
        }"""

        cls.hypervisors = Hypervisors.deserialize(cls.hypervisor_json, "json")


class HypervisorsDomainXMLTest(unittest.TestCase, HypervisorsDomainTest):

    @classmethod
    def setUp(cls):
        cls.hypervisor_xml = """<?xml version="1.0" encoding="UTF-8"?>
        <hypervisors>
                <hypervisor
                    vcpus_used="2" hypervisor_type="xen"
                    local_gb_used="21" hypervisor_hostname="hypervisor_test"
                    memory_mb_used="4608" memory_mb="12285"
                    current_workload="0" vcpus="0" cpu_info="2"
                    running_vms="2" free_disk_gb="888"
                    hypervisor_version="6000000" disk_available_least="None"
                    local_gb="909" free_ram_mb="7677" id="1">
                        <service host="parentcell" id="7" />
                </hypervisor>
        </hypervisors>"""
        cls.hypervisors = Hypervisors.deserialize(cls.hypervisor_xml, "xml")
