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


class PairingBehaviors(object):

    def __init__(self, client, cleanup_client, config):
        super(PairingBehaviors, self).__init__()
        self.client = client
        self.cleanup_client = cleanup_client
        self.pairing_config = config
        self.worker_ids = []

    def remove_created_workers(self):
        self.cleanup_client.connect()
        self.cleanup_client.auth()
        for worker_id in self.worker_ids:
            self.cleanup_client.remove_worker(worker_id)
        self.cleanup_client.disconnect()
        self.worker_ids = []

    def pair_worker_from_config(self, hostname=None, ip_v4=None, ip_v6=None,
                                personality=None, status=None, os_type=None,
                                memory_mb=None, arch=None, cpu_cores=None,
                                load_average=None, disks=None):
        resp = self.pair_worker(
            hostname=hostname or self.pairing_config.hostname,
            ip_v4=ip_v4 or self.pairing_config.ip_v4,
            ip_v6=ip_v6 or self.pairing_config.ip_v6,
            personality=personality or self.pairing_config.personality,
            status='new',
            os_type=os_type or self.pairing_config.os_type,
            memory_mb=memory_mb or self.pairing_config.memory_mb,
            arch=arch or self.pairing_config.arch,
            cpu_cores=cpu_cores or self.pairing_config.cpu_cores,
            load_average=load_average or self.pairing_config.load_average,
            disks=disks or self.pairing_config.disks)

        return resp

    def pair_worker(self, hostname=None, ip_v4=None, ip_v6=None,
                    personality=None, status=None, os_type=None,
                    memory_mb=None, arch=None, cpu_cores=None,
                    load_average=None, disks=None):

        response = self.client.pair(
            hostname=hostname,
            ip_v4=ip_v4,
            ip_v6=ip_v6,
            personality=personality,
            status=status,
            os_type=os_type,
            memory_mb=memory_mb,
            arch=arch,
            cpu_cores=cpu_cores,
            load_average=load_average,
            disks=disks)

        # Store information so we can remove all workers later
        if response.entity is not None:
            self.worker_ids.append(response.entity.worker_id)

        return response
