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

from cafe.engine.http.client import AutoMarshallingHTTPClient

from cloudcafe.stacktach.v2.stacky_api.models.stacky_api import \
    (Deployments, EventNames, HostNames, TimingsSummaries,
     UuidTimingsSummaries, EventNameTimings, EventDetails, ImageEventDetails,
     KpiDetails, WatchEvents, Reports, EventIdDetails)


class StackTachClient(AutoMarshallingHTTPClient):

    def __init__(self, url, serialize_format, deserialize_format=None):
        super(StackTachClient, self).__init__(serialize_format,
                                              deserialize_format)
        self.url = url
        ct = '{content_type}/{content_subtype}'.format(
            content_type='application',
            content_subtype=self.serialize_format)
        accept = '{content_type}/{content_subtype}'.format(
            content_type='application',
            content_subtype=self.deserialize_format)
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept

    def get_event_names(self, service, requestslib_kwargs=None):
        """
        @summary: Retrieves Event Names that are known
        @param service: Service/Product e.g. nova or glance
        @type service: String
        @return: List of event names
        @rtype:  Response Object

            GET
            stacky/events/?service={service}
        """
        params = {'service': service}
        url = '{0}{1}'.format(self.url, '/stacky/events/')
        return self.request('GET', url, params=params,
                            response_entity_type=EventNames,
                            requestslib_kwargs=requestslib_kwargs)

    def get_host_names(self, service, requestslib_kwargs=None):
        """
        @summary: Retrieves Host Names that are known
        @param service: Service/Product e.g. nova or glance
        @type service: String
        @return: List of host names
        @rtype:  Response Object

            GET
            stacky/hosts/?service={service}
        """
        params = {'service': service}
        url = '{0}{1}'.format(self.url, '/stacky/hosts/')
        return self.request('GET', url, params=params,
                            response_entity_type=HostNames,
                            requestslib_kwargs=requestslib_kwargs)

    def get_deployments(self, requestslib_kwargs=None):
        """
        @summary: Retrieves Deployments that are known
        @return: List of Deployments
        @rtype:  Response Object

            GET
            stacky/deployments/
        """
        url = '{0}{1}'.format(self.url, '/stacky/deployments/')
        return self.request('GET', url, response_entity_type=Deployments,
                            requestslib_kwargs=requestslib_kwargs)

    def get_timings_summary(self, requestslib_kwargs=None):
        """
        @summary: Retrieves summarized timings for all events
        @return: List of timings
        @rtype:  Response Object

            GET
            stacky/summary/
        """
        url = '{0}{1}'.format(self.url, '/stacky/summary/')
        return self.request('GET', url, response_entity_type=TimingsSummaries,
                            requestslib_kwargs=requestslib_kwargs)

    def get_timings_for_uuid(self, uuid, requestslib_kwargs=None):
        """
        @summary: Retrieves summarized timings for a given server
        @param uuid: The uuid of an existing instance.
        @type uuid: String
        @return: List of timings for the server
        @rtype:  Response Object

            GET
            stacky/timings/uuid/?uuid={uuid}
        """
        params = {'uuid': uuid}
        url = '{0}{1}'.format(self.url, '/stacky/timings/uuid/')
        return self.request('GET', url, params=params,
                            response_entity_type=UuidTimingsSummaries,
                            requestslib_kwargs=requestslib_kwargs)

    def get_timings_for_event_name(self, event, requestslib_kwargs=None):
        """
        @summary: Retrieves timings for a given event name
        @param event: The name of an event
        @type event: String
        @return: List of timings for the event name
        @rtype:  Response Object

            GET
            stacky/timings/?name={event}
        """
        params = {'name': event}
        url = '{0}{1}'.format(self.url, '/stacky/timings/')
        return self.request('GET', url, params=params,
                            response_entity_type=EventNameTimings,
                            requestslib_kwargs=requestslib_kwargs)

    def get_events_for_uuid(self, service, uuid, requestslib_kwargs=None,
                            limit=100):
        """
        @summary: Retrieves events related to a given server
        @param uuid: The uuid of an existing instance.
        @type uuid: String
        @param service: Service/Product e.g. nova or glance
        @type service: String
        @param limit: Max number of events to return
        @type limit: int
        @return: List of events for the server
        @rtype:  Response Object

            GET
            stacky/uuid/?uuid={uuid}&service={service}
        """
        response_entity_type = EventDetails
        if service == 'glance':
            response_entity_type = ImageEventDetails
        params = {'uuid': uuid, 'service': service, 'limit': limit}
        url = '{0}{1}'.format(self.url, '/stacky/uuid/')
        return self.request('GET', url, params=params,
                            response_entity_type=response_entity_type,
                            requestslib_kwargs=requestslib_kwargs)

    def get_events_for_request_id(self, request_id, requestslib_kwargs=None):
        """
        @summary: Retrieves events related to a given request id
        @param request_id:  An identifier of an event given by the API
        @type request_id: String
        @return: List of events for the request id
        @rtype:  Response Object

            GET
            stacky/request/?request_id={request_id}
        """
        params = {'request_id': request_id}
        url = '{0}{1}'.format(self.url, '/stacky/request/')
        return self.request('GET', url, params=params,
                            response_entity_type=EventDetails,
                            requestslib_kwargs=requestslib_kwargs)

    def get_kpi(self, requestslib_kwargs=None):
        """
        @summary: Retrieves key performance indicators
        @return: List of key performance indicators
        @rtype:  Response Object

            GET
            stacky/kpi/
        """
        url = '{0}{1}'.format(self.url, '/stacky/kpi/')
        return self.request('GET', url, response_entity_type=KpiDetails,
                            requestslib_kwargs=requestslib_kwargs)

    def get_kpi_for_tenant_id(self, tenant_id, requestslib_kwargs=None):
        """
        @summary: Retrieves key performance indicators for a tenant
        @param tenant_id:  The id of an existing tenant.
        @type tenant_id: String
        @return: List of key performance indicators for a tenant
        @rtype:  Response Object

            GET
            stacky/kpi/{tenant_id}/
        """
        url = '{0}{1}{2}'.format(self.url, '/stacky/kpi/', tenant_id)
        return self.request('GET', url, response_entity_type=KpiDetails,
                            requestslib_kwargs=requestslib_kwargs)

    def get_watch_events(self, service, deployment_id,
                         requestslib_kwargs=None):
        """
        @summary: Retrieves current events coming from a given deloyment
        @param deployment_id:  An identifier of a deployment
        @type deployment_id: String
        @param service: Service/Product e.g. nova or glance
        @type service: String
        @return: List of events for a deployment
        @rtype:  Response Object

            GET
            stacky/watch/{deployment_id}/?service={service}
        """
        params = {'service': service}
        url = '{0}{1}{2}/'.format(self.url, '/stacky/watch/', deployment_id)
        return self.request('GET', url, params=params,
                            response_entity_type=WatchEvents,
                            requestslib_kwargs=requestslib_kwargs)

    def get_event_id_details(self, event_id, service, requestslib_kwargs=None):
        """
        @summary: Retrieves details of a given event
        @param event_id:  An identifier of an event within the StackTach DB
        @type event_id: String
        @return: Details of an event
        @rtype:  Response Object
        @note: response formatted for command line

            GET
            stacky/show/{event_id}/?service={service}
        """
        params = {'service': service}
        url = '{0}{1}{2}'.format(self.url, '/stacky/show/', event_id)
        return self.request('GET', url, params=params,
                            response_entity_type=EventIdDetails,
                            requestslib_kwargs=requestslib_kwargs)

    def get_event_type_details(self, event_type, service,
                               requestslib_kwargs=None):
        """
        @summary: Retrieves details of a given event
        @param event_type:  The name of an event within the StackTach DB
        @type event_type: String
        @return: Details of an event
        @rtype:  Response Object
        @note: response formatted for command line
            GET
            stacky/search/?field={event}&value={event_type}
            &service={service}&limit={limit}
        """
        params = {'field': 'event', 'value': event_type,
                  'service': service, 'limit': 10}
        url = "{url}/stacky/search".format(url=self.url)
        return self.request('GET', url, params=params,
                            response_entity_type=ImageEventDetails,
                            requestslib_kwargs=requestslib_kwargs)

    def get_reports(self, requestslib_kwargs=None):
        """
        @summary: Retrieves a list of available reports
        @return: List of reports
        @rtype:  Response Object

            GET
            stacky/reports/
        """
        url = '{0}{1}'.format(self.url, '/stacky/reports/')
        return self.request('GET', url,
                            response_entity_type=Reports,
                            requestslib_kwargs=requestslib_kwargs)

    def get_report_details(self, report_id, requestslib_kwargs=None):
        """
        @summary: Retrieves detailed report
        @param report_id:  An identifier of a report
        @type report_id: String
        @return: Detailed report
        @rtype:  Response Object

            GET
            stacky/report/{report_id}/
        """
        url = '{0}{1}{2}'.format(self.url, '/stacky/report/', str(report_id))
        return self.request('GET', url,
                            requestslib_kwargs=requestslib_kwargs)
