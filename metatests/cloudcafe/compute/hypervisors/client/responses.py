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


class HypervisorsClientMockResponse(object):

    @classmethod
    def list_hypervisors(cls):
        return ('{"hypervisors": [{'
                '"id": 1, '
                '"hypervisor_hostname": "hypervisor_test"}'
                ']}')

    @classmethod
    def list_hypervisor_servers(cls):
        return ('{"hypervisors": [{ '
                '"id": 1,'
                '"hypervisor_hostname": "hypervisor_test",'
                '"servers":'
                '[{"uuid": "b1ea4f1b-201c-47c5-95b9-c6fe2df39af0",'
                '"name": "instance-00000003"},'
                '{"uuid": "9327b134-b1f5-43ec-a8f1-2b6eb153c739",'
                '"name": "instance-00000005"}}]}]}')

    @classmethod
    def list_hypervisors_in_detail(cls):
        return """
        {
            "hypervisors":[
                {
                "service":
                {
                    "host":"parentcell",
                    "id":7
                },
                "vcpus_used":2,
                "hypervisor_type":"xen",
                "local_gb_used":21,
                "hypervisor_hostname":"hypervisor_test",
                "memory_mb_used":4608,
                "memory_mb":12285,
                "current_workload":0,
                "vcpus":0,
                "cpu_info": 2,
                "running_vms":2,
                "free_disk_gb":888,
                "hypervisor_version":6000,
                "disk_available_least":"None",
                "local_gb":909,
                "free_ram_mb":7677,
                "id":1
                }
            ]
        }"""
