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

import time

from cafe.engine.behaviors import BaseBehavior
from cloudcafe.compute.common.exceptions import TimeoutException


class StackTachDBBehavior(BaseBehavior):

    def __init__(self, stacktach_db_client, stacktach_config):

        super(StackTachDBBehavior, self).__init__()
        self.config = stacktach_config
        self.client = stacktach_db_client

    def wait_for_launched_at(self, server_id, interval_time=10, timeout=200):
        '''
        @summary: Polls Launch launched_at field until it is populated
        '''

        launch_resp = self.client.list_launches_for_uuid(instance=server_id)
        launches = launch_resp.entity

        # Go through each of the launches and check that
        # the launched_at attribute exists and is populated
        for launch_obj in launches:
            found_launched_at = False
            time_waited = 0
            while ((not found_launched_at or
                    not hasattr(launch_obj, 'launched_at')) and
                    (time_waited <= timeout)):
                resp = self.client.list_launches_for_uuid(instance=server_id)
                items = resp.entity
                # Iterate over response and match on launch id
                items = [item for item in items if item.id == launch_obj.id]
                try:
                    found_launched_at = items[0].launched_at
                except:
                    pass
                time.sleep(interval_time)
                time_waited += interval_time
            if time_waited > timeout:
                raise TimeoutException(
                    "Timed Out. Server with uuid {0} timed "
                    "out waiting for Launch entry launched_at field to be "
                    "populated after {1} seconds. response: {2}"
                    .format(server_id, timeout, launch_resp))
        return launch_resp
