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

from cloudcafe.stacktach.stacktach_db_api.models.stacktach_db_api import \
    (Launch as ResponseLaunch,
     Delete as ResponseDelete,
     Exist as ResponseExist)


class StackTachDBClient(AutoMarshallingRestClient):

    def __init__(self, db_url, serialize_format, deserialize_format=None):
        super(StackTachDBClient, self).__init__(serialize_format,
                                                deserialize_format)
        self.url = db_url
        ct = '{content_type}/{content_subtype}'.format(
            content_type='application',
            content_subtype=self.serialize_format)
        accept = '{content_type}/{content_subtype}'.format(
            content_type='application',
            content_subtype=self.deserialize_format)
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept

    def list_launches(self, requestslib_kwargs=None):
        """
        @summary: Retrieves all server launches
        @return: Dictionary key:'launches' with value as a list of launches
        @rtype:  Response Object

            GET
            /db/usage/launches/
        """
        url = "{0}{1}".format(self.url, '/db/usage/launches/')
        return self.request('GET', url,
                            response_entity_type=ResponseLaunch,
                            requestslib_kwargs=requestslib_kwargs)

    def list_launches_for_uuid(self, instance, requestslib_kwargs=None):
        """
        @summary: Retrieves server launches for a given uuid
        @param instance: The uuid of the server
        @type instance: String
        @return: Dictionary key:'launches' with value as a list of launches
                 for a given instance
        @rtype:  Response Object

            GET
            /db/usage/launches/?instance={uuid}
        """
        params = {'instance': instance}
        url = "{0}{1}".format(self.url, '/db/usage/launches/')
        return self.request('GET', url, params=params,
                            response_entity_type=ResponseLaunch,
                            requestslib_kwargs=requestslib_kwargs)

    def list_deletes(self, requestslib_kwargs=None):
        """
        @summary: Retrieves all known server deletes
        @return: Dictionary key:'deletes' with value as a list of deletes
        @rtype:  Response Object

            GET
            /db/usage/deletes/
        """
        url = "{0}{1}".format(self.url, '/db/usage/deletes/')
        return self.request('GET', url,
                            response_entity_type=ResponseDelete,
                            requestslib_kwargs=requestslib_kwargs)

    def list_deletes_for_uuid(self, instance, requestslib_kwargs=None):
        """
        @summary: Retrieves server deletes for a given uuid
        @param instance: The uuid of the server
        @type instance: String
        @return: Dictionary key:'deletes' with value as a list of deletes
                 for a given instance
        @rtype:  Response Object

            GET
            /db/usage/deletes/?instance={uuid}
        """
        params = {'instance': instance}
        url = "{0}{1}".format(self.url, '/db/usage/deletes/')
        return self.request('GET', url, params=params,
                            response_entity_type=ResponseDelete,
                            requestslib_kwargs=requestslib_kwargs)

    def list_exists(self, requestslib_kwargs=None):
        """
        @summary: Retrieves all known exists events
        @return: Dictionary key:'exists' with value as a list of exists events
        @rtype:  Response Object

            GET
            /db/usage/exists/
        """
        url = "{0}{1}".format(self.url, '/db/usage/exists/')
        return self.request('GET', url,
                            response_entity_type=ResponseExist,
                            requestslib_kwargs=requestslib_kwargs)

    def list_exists_for_uuid(self, instance, requestslib_kwargs=None):
        """
        @summary: Retrieves all known exists events for server
        @param instance: The uuid of the server
        @type instance: String
        @return: Dictionary key:'exists' with value as a list of exists events
                 for a given instance
        @rtype:  Response Object

            GET
            /db/usage/exists/?instance={uuid}
        """
        params = {'instance': instance}
        url = "{0}{1}".format(self.url, '/db/usage/exists/')
        return self.request('GET', url, params=params,
                            response_entity_type=ResponseExist,
                            requestslib_kwargs=requestslib_kwargs)

    def get_launch(self, event_id, requestslib_kwargs=None):
        """
        @summary: Retrieves launch details of a given id
        @param event_id:  An identifier of an event within the StackTach DB
        @type event_id: String
        @return: Launch details of an event
        @rtype:  Response Object

            GET
            /db/usage/launches/{event_id}/
        """
        url = "{0}{1}{2}".format(self.url, '/db/usage/launches/', event_id)
        return self.request('GET', url,
                            response_entity_type=ResponseLaunch,
                            requestslib_kwargs=requestslib_kwargs)

    def get_delete(self, event_id, requestslib_kwargs=None):
        """
        @summary: Retrieves delete details of a given id
        @param event_id:  An identifier of an event within the StackTach DB
        @type event_id: String
        @return: Delete details of an event
        @rtype:  Response Object

            GET
            /db/usage/deletes/{event_id}/
        """
        url = "{0}{1}{2}".format(self.url, '/db/usage/deletes/', event_id)
        return self.request('GET', url,
                            response_entity_type=ResponseDelete,
                            requestslib_kwargs=requestslib_kwargs)

    def get_exist(self, event_id, requestslib_kwargs=None):
        """
        @summary: Retrieves exists event details of a given id
        @param event_id:  An identifier of an event within the StackTach DB
        @type event_id: String
        @return: Launch details of an event
        @rtype:  Response Object

            GET
            /db/usage/exists/{event_id}/
        """
        url = "{0}{1}{2}".format(self.url, '/db/usage/exists/', event_id)
        return self.request('GET', url,
                            response_entity_type=ResponseExist,
                            requestslib_kwargs=requestslib_kwargs)

    def get_launches_by_date_min(self, launched_at_min=None,
                                 requestslib_kwargs=None):
        """
        @summary: Retrieves launch events details filtered by minimum date
        @param launched_at_min: A string formatted as
            YYYY-MM-DD HH:MM:SS.mmmmmm
        @type launched_at_min: String
        @return: Dictionary, key:'launches' with value: an unordered list of
            launch events starting at launched_at_min and ending at
            latest record
        @rtype:  Response Object

            GET
            /db/usage/launches/?launched_at_min={launched_at_min}
        """
        params = {'launched_at_min': launched_at_min}
        url = "{0}{1}".format(self.url, '/db/usage/launches/')
        return self.request('GET', url, params=params,
                            response_entity_type=ResponseLaunch,
                            requestslib_kwargs=requestslib_kwargs)

    def get_launches_by_date_max(self, launched_at_max=None,
                                 requestslib_kwargs=None):
        """
        @summary: Retrieves launch events details filtered by maximum date
        @param launched_at_max: A string formatted as
            YYYY-MM-DD HH:MM:SS.mmmmmm
        @type launched_at_max: String
        @return: Dictionary, key:'launches' with value: an unordered list of
            launch events starting from earliest record and ending at
            launched_at_max
        @rtype:  Response Object

            GET
            /db/usage/launches/?launched_at_max={launched_at_max}
        """
        params = {'launched_at_max': launched_at_max}
        url = "{0}{1}".format(self.url, '/db/usage/launches/')
        return self.request('GET', url, params=params,
                            response_entity_type=ResponseLaunch,
                            requestslib_kwargs=requestslib_kwargs)

    def get_launches_by_date_min_and_date_max(self, launched_at_min=None,
                                              launched_at_max=None,
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
        @rtype:  Response Object

            GET
            /db/usage/launches/?launched_at_min={launched_at_min}
                &launched_at_max={launched_at_max}
        """
        params = {'launched_at_min': launched_at_min,
                  'launched_at_max': launched_at_max}
        url = "{0}{1}".format(self.url, '/db/usage/launches/')
        return self.request('GET', url, params=params,
                            response_entity_type=ResponseLaunch,
                            requestslib_kwargs=requestslib_kwargs)

    def get_deletes_by_date_min(self, deleted_at_min=None,
                                requestslib_kwargs=None):
        """
        @summary: Retrieves delete events details filtered by minimum date
        @param deleted_at_min: A string formatted as
            YYYY-MM-DD HH:MM:SS.mmmmmm
        @type deleted_at_min: String
        @return: Dictionary, key:'deletes' with value: an unordered list of
            delete events starting at deleted_at_min and ending at
            latest record
        @rtype:  Response Object

            GET
            /db/usage/deletes/?deleted_at_min={deleted_at_min}
        """
        params = {'deleted_at_min': deleted_at_min}
        url = "{0}{1}".format(self.url, '/db/usage/deletes/')
        return self.request('GET', url, params=params,
                            response_entity_type=ResponseDelete,
                            requestslib_kwargs=requestslib_kwargs)

    def get_deletes_by_date_max(self, deleted_at_max=None,
                                requestslib_kwargs=None):
        """
        @summary: Retrieves delete events details filtered by maximum date
        @param deleted_at_max: A string formatted as
            YYYY-MM-DD HH:MM:SS.mmmmmm
        @type deleted_at_max: String
        @return: Dictionary, key:'deletes' with value: an unordered list of
            delete events starting from earliest record and ending at
            deleted_at_max
        @rtype:  Response Object

            GET
            /db/usage/deletes/?deleted_at_max={deleted_at_max}
        """
        params = {'deleted_at_max': deleted_at_max}
        url = "{0}{1}".format(self.url, '/db/usage/deletes/')
        return self.request('GET', url, params=params,
                            response_entity_type=ResponseDelete,
                            requestslib_kwargs=requestslib_kwargs)

    def get_deletes_by_date_min_and_date_max(self, deleted_at_min=None,
                                             deleted_at_max=None,
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
        @rtype:  Response Object

            GET
            /db/usage/deletes/?deleted_at_min={deleted_at_min}
                &deleted_at_max={deleted_at_max}
        """
        params = {'deleted_at_min': deleted_at_min,
                  'deleted_at_max': deleted_at_max}
        url = "{0}{1}".format(self.url, '/db/usage/deletes/')
        return self.request('GET', url, params=params,
                            response_entity_type=ResponseDelete,
                            requestslib_kwargs=requestslib_kwargs)
