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

from cafe.engine.behaviors import BaseBehavior


class StackTachBehavior(BaseBehavior):

    def __init__(self, stacktach_client, stacktach_config):

        super(StackTachDBBehavior, self).__init__()
        self.config = stacktach_config
        self.client = stacktach_client

    def get_uuid_from_event_id_details(self, event_id='1'):
        '''
        @summary: Gets the uuid from the event id details
        @param event_id: The event_id in Stacky
        @type event_id: String
        @return: uuid
        @rtype: String
        '''
        response = self.client.get_event_id_details(event_id)
        return response.entity.uuid

    def get_report_id_by_report_name(self, report_name):
        '''
        @summary: Gets the report id by report name from a
            list of available reports
        @param report_name: Name of the report
        @type report_name: String
        @return: report_id
        @rtype: String
        '''
        reports = self.client.get_reports().entity
        for report in reports:
            if report.name == report_name:
                return report.report_id
        else:
            msg = ("{0} report was not found in reports list."
                   .format(report_name))
            raise Exception(msg)
