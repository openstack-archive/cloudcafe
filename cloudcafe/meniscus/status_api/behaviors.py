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
from datetime import datetime
from cafe.engine.behaviors import BaseBehavior


class StatusAPIBehaviors(BaseBehavior):

    def __init__(self, status_client, pairing_config):
        super(StatusAPIBehaviors, self).__init__()
        self.status_client = status_client
        self.pairing_config = pairing_config

    def update_load_average(self, worker_id, worker_token,
                            one, five, fifteen):
        response = self.status_client.update_status(
            worker_id=worker_id, worker_token=worker_token,
            status='new',
            os_type=self.pairing_config.os_type,
            memory_mb=self.pairing_config.memory_mb,
            architecture=self.pairing_config.arch,
            cpu_cores=self.pairing_config.cpu_cores,
            timestamp=datetime.now().isoformat(),
            one=one, five=five, fifteen=fifteen,
            disks={})
        return response

    def update_status_from_config(self, worker_id, worker_token, status=None,
                                  os_type=None, memory_mb=None,
                                  architecture=None, cpu_cores=None,
                                  timestamp=None, one=None, five=None,
                                  fifteen=None, disks=None):

        response = self.status_client.update_status(
            worker_id=worker_id, worker_token=worker_token,
            status=status or 'new',
            os_type=os_type or self.pairing_config.os_type,
            memory_mb=memory_mb or self.pairing_config.memory_mb,
            architecture=architecture or self.pairing_config.arch,
            cpu_cores=cpu_cores or self.pairing_config.cpu_cores,
            timestamp=timestamp or datetime.now().isoformat(),
            one=one or 0.0, five=five or 0.0, fifteen=fifteen or 0.0,
            disks=disks or {})
        return response
