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
from cafe.engine.clients.rest import AutoMarshallingRestClient
from cloudcafe.meniscus.common.models.system \
    import SystemInfo, DiskUsage, LoadAverage
from cloudcafe.meniscus.coordinator_api.models.pairing \
    import WorkerRegistration, WorkerPairing
from cloudcafe.meniscus.coordinator_api.models.routing import AllRoutes
from cloudcafe.meniscus.coordinator_api.models.status import UpdateStatus


class PairingClient(AutoMarshallingRestClient):
    def __init__(self, url, api_version, auth_token, serialize_format=None,
                 deserialize_format=None):
        super(PairingClient, self).__init__(serialize_format,
                                            deserialize_format)
        self.url = url
        self.api_version = api_version
        self.auth_token = auth_token

    def pair(self, hostname, ip_v4, ip_v6, personality, status,
             os_type, memory_mb, arch, cpu_cores, load_average, disks):
        """
        POST {base}/{version}/pairing
        @summary Registers a worker on the coordinator
        @return:
        """
        remote = '{base}/{version}/pairing'.format(base=self.url,
                                                   version=self.api_version)
        headers = {'X-AUTH-TOKEN': self.auth_token}

        # Setup Request objects.
        disk_usage = DiskUsage._dict_to_obj(disks)
        load_average = LoadAverage._dict_to_obj(load_average)
        system_info = SystemInfo(disk_usage=disk_usage,
                                 os_type=os_type,
                                 memory_mb=memory_mb,
                                 architecture=arch,
                                 cpu_cores=cpu_cores,
                                 load_average=load_average)
        request_obj = WorkerRegistration(
            hostname=hostname, ip_v4=ip_v4, ip_v6=ip_v6,
            personality=personality, status=status, system_info=system_info)

        # Pair request
        resp = self.request('POST',
                            url=remote,
                            headers=headers,
                            request_entity=request_obj,
                            response_entity_type=WorkerPairing)
        return resp

    def get_routing(self, worker_id, worker_token):
        """
        GET {base}/{version}/worker/{worker_id}/routes
        @summary Retrieves worker routing information
        @return:
        """
        remote = '{base}/{version}/worker/{worker_id}/routes'.format(
            base=self.url,
            version=self.api_version,
            worker_id=worker_id)
        headers = {'WORKER-TOKEN': worker_token}

        resp = self.request('GET', remote, headers,
                            response_entity_type=AllRoutes)
        return resp

    def update_status(self, worker_id, worker_token, status):
        """
        PUT {base}/{version}/worker/{worker_id}/status
        @return:
        """
        remote = '{base}/{version}/worker/{worker_id}/status'.format(
            base=self.url,
            version=self.api_version,
            worker_id=worker_id)
        headers = {'WORKER-TOKEN': worker_token}
        update_obj = UpdateStatus(status)

        # Update request
        resp = self.request('PUT', remote, headers, request_entity=update_obj)
        return resp
