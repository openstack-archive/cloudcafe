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

    def get_request_id_from_launches(self):
        '''
        @summary: Gets a request_id from list of active launches
        @return: request_id
        @rtype: String
        '''
        response = self.client.list_launches()
        try:
            request_id = response.entity[0].request_id
        except AttributeError as err:
            raise Exception("Request id was not found in response: {0}"
                            "error: {1}".format(response, err))
        return request_id

    def get_active_tenant_id_from_launches(self):
        '''
        @summary: Gets the tenant_id from list of active launches
        @return: tenant_id
        @rtype: String
        '''
        response = self.client.list_launches()
        try:
            tenant_id = response.entity[0].tenant
        except AttributeError as err:
            raise Exception("Tenant id was not found in response: {0}"
                            "error: {1}".format(response, err))
        return tenant_id

    def list_launches_for_uuid(self, instance, requestslib_kwargs=None):
        """
        @summary: Retrieves server launches for a given uuid
        @param instance: The uuid of the server
        @type instance: String
        @return: Dictionary key:'launches' with value as a list of launches
                 for a given instance
        @rtype: ResponseLaunch Object

        """
        response = self.client.list_launches(instance=instance,
                                             requestslib_kwargs=None)
        return response

    def list_launches_by_date_min(self, launched_at_min,
                                  requestslib_kwargs=None):
        """
        @summary: Retrieves launch events details filtered by minimum date
        @param launched_at_min: A string formatted as
            YYYY-MM-DD HH:MM:SS.mmmmmm
        @type launched_at_min: String
        @return: Dictionary, key:'launches' with value: an unordered list of
            launch events starting at launched_at_min and ending at
            latest record
        @rtype: ResponseLaunch Object
        """
        response = self.client.list_launches(launched_at_min=launched_at_min,
                                             requestslib_kwargs=None)
        return response

    def list_launches_by_date_max(self, launched_at_max,
                                  requestslib_kwargs=None):
        """
        @summary: Retrieves launch events details filtered by maximum date
        @param launched_at_max: A string formatted as
            YYYY-MM-DD HH:MM:SS.mmmmmm
        @type launched_at_max: String
        @return: Dictionary, key:'launches' with value: an unordered list of
            launch events starting from earliest record and ending at
            launched_at_max
        @rtype: ResponseLaunch Object
        """
        response = self.client.list_launches(launched_at_max=launched_at_max,
                                             requestslib_kwargs=None)
        return response

    def list_launches_by_date_min_and_date_max(self, launched_at_min,
                                               launched_at_max,
                                               requestslib_kwargs=None):
        """
        @summary: Retrieves launch events details filtered by minimum date
            and maximum date
        @param launched_at_min: A string formatted as
            YYYY-MM-DD HH:MM:SS.mmmmmm
        @type launched_at_min: String
        @param launched_at_max: A string formatted as
            YYYY-MM-DD HH:MM:SS.mmmmmm
        @type launched_at_max: String
        @return: Dictionary, key:'launches' with value: an unordered list of
            launch events starting at launched_at_min and ending at
            launched_at_max
        @rtype: ResponseLaunch Object
        """
        response = self.client.list_launches(launched_at_min=launched_at_min,
                                             launched_at_max=launched_at_max,
                                             requestslib_kwargs=None)
        return response

    def list_deletes_by_date_min(self, deleted_at_min,
                                 requestslib_kwargs=None):
        """
        @summary: Retrieves delete events details filtered by minimum date
        @param deleted_at_min: A string formatted as
            YYYY-MM-DD HH:MM:SS.mmmmmm
        @type deleted_at_min: String
        @return: Dictionary, key:'deletes' with value: an unordered list of
            delete events starting at deleted_at_min and ending at
            latest record
        @rtype: ResponseDelete Object
        """
        response = self.client.list_deletes(deleted_at_min=deleted_at_min,
                                            requestslib_kwargs=None)

    def list_deletes_by_date_max(self, deleted_at_max,
                                 requestslib_kwargs=None):
        """
        @summary: Retrieves delete events details filtered by maximum date
        @param deleted_at_max: A string formatted as
            YYYY-MM-DD HH:MM:SS.mmmmmm
        @type deleted_at_max: String
        @return: Dictionary, key:'deletes' with value: an unordered list of
            delete events starting from earliest record and ending at
            deleted_at_max
        @rtype: ResponseDelete Object
        """
        response = self.client.list_deletes(deleted_at_max=deleted_at_max,
                                            requestslib_kwargs=None)

    def list_deletes_by_date_min_and_date_max(self, deleted_at_min,
                                              deleted_at_max,
                                              requestslib_kwargs=None):
        """
        @summary: Retrieves delete events details filtered by minimum date
            and maximum date
        @param deleted_at_min: A string formatted as
            YYYY-MM-DD HH:MM:SS.mmmmmm
        @type deleted_at_min: String
        @param deleted_at_max: A string formatted as
            YYYY-MM-DD HH:MM:SS.mmmmmm
        @type deleted_at_max: String
        @return: Dictionary, key:'deletes' with value: an unordered list of
            delete events starting at deleted_at_min and ending at
            deleted_at_max
        @rtype: ResponseDelete Object
        """
        response = self.client.list_deletes(deleted_at_min=deleted_at_min,
                                            deleted_at_max=deleted_at_max,
                                            requestslib_kwargs=None)

    def list_exists_for_uuid(self, instance, requestslib_kwargs=None):
        """
        @summary: Retrieves all known exists events for server
        @param instance: The uuid of the server
        @type instance: String
        @return: Dictionary key:'exists' with value as a list of exists events
                 for a given instance
        @rtype: ResponseExist Object

            GET
            /db/usage/exists/?instance={uuid}
        """
        response = self.client.list_exists(instance=instance,
                                           requestslib_kwargs=None)

    def wait_for_launched_at(self, server_id, interval_time=10, timeout=200):
        '''
        @summary: Polls Launch launched_at field until it is populated
        @param server_id: The uuid of the instance
        @type server_id: String
        @param interval_time: Time in seconds to wait between tries
        @type inverval_time: Int
        @param timeout: Time in seconds before timing out
        @type timepout: Int
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
                except AttributeError:
                    self._log("Did not find launched at this time around.")
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
