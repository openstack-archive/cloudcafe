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
from cloudcafe.meniscus.common.models.system import SystemInfo
from cloudcafe.meniscus.status_api.models.status \
    import (AllWorkersStatus, WorkerStatus, WorkerLoadAverage,
            WorkerDiskUsage, WorkerStatusUpdate)


class WorkerStatusClient(AutoMarshallingRestClient):

    def __init__(self, url, api_version, serialize_format,
                 deserialize_format):
        super(WorkerStatusClient, self).__init__(serialize_format,
                                                 deserialize_format)
        self.url = url
        self.api_version = api_version

    def _get_remote_url(self, worker_id):
        url = '{base}/{version}/worker/{worker_id}/status'.format(
            base=self.url, version=self.api_version, worker_id=worker_id)
        return url

    def get_worker_status(self, worker_id):
        url = '{base}/{version}/worker/{worker_id}/status'.format(
            base=self.url, version=self.api_version, worker_id=worker_id)
        resp = self.request('GET', url, response_entity_type=WorkerStatus)
        return resp

    def get_all_worker_statuses(self):
        url = '{base}/{version}/status'.format(base=self.url,
                                               version=self.api_version)
        resp = self.request('GET', url, response_entity_type=AllWorkersStatus)
        return resp
