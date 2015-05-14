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

        super(StackTachBehavior, self).__init__()
        self.config = stacktach_config
        self.client = stacktach_client

    def get_uuid_from_event_id_details(self, service, event_id='1'):
        """
        @summary: Gets the uuid of an instance from the event id details
        @param event_id: The event_id in Stacky
        @type event_id: String
        @param service: Service/Product e.g. nova or glance
        @type service: String
        @return: uuid of instance
        @rtype: String
        """
        response = self.client.get_event_id_details(event_id=event_id,
                                                    service=service)
        try:
            uuid = response.entity[0].uuid
        except AttributeError as err:
            raise Exception("UUID was not found in response: {0}"
                            "\nError: {1}".format(vars(response), err))
        return uuid

    def get_request_id_from_event_id_details(self, service, event_id='1'):
        """
        @summary: Gets the request_id from the event id details
        @param event_id: The event_id in Stacky
        @type event_id: String
        @param service: Service/Product e.g. nova or glance
        @type service: String
        @return: request_id
        @rtype: String
        """
        response = self.client.get_event_id_details(event_id=event_id,
                                                    service=service)
        try:
            request_id = response.entity[0].request_id
        except AttributeError as err:
            raise Exception("Request id was not found in response: {0}"
                            "\n Error: {1}".format(vars(response), err))
        return request_id

    def get_event_id_from_event_type_details(self, service, event_type):
        """
        @summary: Gets the event_id from the event type details
        @param event_type: The event in Stacky
        @type event_type: String
        @return: event_id
        @rtype: String
        """
        response = self.client.get_event_type_details(event_type=event_type,
                                                      service=service)
        try:
            event_id = response.entity[0].event_id
        except AttributeError as err:
            raise Exception("Event id was not found in response: {0}"
                            "\n Error: {1}".format(vars(response), err))
        return event_id

    def get_report_id_by_report_name(self, report_name):
        """
        @summary: Gets the report id by report name from a
            list of available reports
        @param report_name: Name of the report
        @type report_name: String
        @return: report_id
        @rtype: String
        """
        response = self.client.get_reports()
        reports = response.entity
        if reports is None:
            raise Exception("Reports was not found in the response: {0}"
                            .format(response))

        for report in reports:
            if report.name == report_name:
                return report.report_id
        else:
            msg = ("{0} report was not found in reports list."
                   .format(report_name))
            self._log.error(msg)
            return None
