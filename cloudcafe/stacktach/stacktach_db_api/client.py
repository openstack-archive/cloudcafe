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

from cloudcafe.stacktach.stacktach_db_api.models.stacktach_db_api import \
    (ServerLaunch, ServerLaunches, ServerDelete, ServerDeletes,
     ServerExist, ServerExists, ImageUsages, ImageDeletes, ImageExists)


class StackTachDBClient(AutoMarshallingHTTPClient):

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

    def get_launch(self, event_id, requestslib_kwargs=None):
        """
        @summary: Retrieves launch details of a given id
        @param event_id:  An identifier of an event within the StackTach DB
        @type event_id: String
        @return: Launch details of an event
        @rtype:  ServerLaunch Object

            GET
            /db/usage/launches/{event_id}/
        """
        url = "{0}{1}{2}".format(self.url, '/db/usage/launches/', event_id)
        return self.request('GET', url,
                            response_entity_type=ServerLaunch,
                            requestslib_kwargs=requestslib_kwargs)

    def get_delete(self, event_id, requestslib_kwargs=None):
        """
        @summary: Retrieves delete details of a given id
        @param event_id:  An identifier of an event within the StackTach DB
        @type event_id: String
        @return: Delete details of an event
        @rtype:  ServerDelete Object

            GET
            /db/usage/deletes/{event_id}/
        """
        url = "{0}{1}{2}".format(self.url, '/db/usage/deletes/', event_id)
        return self.request('GET', url,
                            response_entity_type=ServerDelete,
                            requestslib_kwargs=requestslib_kwargs)

    def get_exist(self, event_id, requestslib_kwargs=None):
        """
        @summary: Retrieves exists event details of a given id
        @param event_id:  An identifier of an event within the StackTach DB
        @type event_id: String
        @return: Launch details of an event
        @rtype:  ServerExist Object

            GET
            /db/usage/exists/{event_id}/
        """
        url = "{0}{1}{2}".format(self.url, '/db/usage/exists/', event_id)
        return self.request('GET', url,
                            response_entity_type=ServerExist,
                            requestslib_kwargs=requestslib_kwargs)

    def list_exists(self, instance=None, requestslib_kwargs=None):
        """
        @summary: Retrieves the latest exists events for all instances
            or for a given instance if defined.
        @param instance: The uuid of the server
        @type instance: String
        @return: Dictionary key:'exists' with value as a list of exists events
        @rtype:  ServerExists Object
        @note: Date filters not supported
            GET
            /db/usage/exists/

            if instance is defined:
            GET
            /db/usage/exists/?instance={uuid}
        """
        params = {}
        if instance:
            params['instance'] = instance

        url = "{0}{1}".format(self.url, '/db/usage/exists/')
        return self.request('GET', url, params=params,
                            response_entity_type=ServerExists,
                            requestslib_kwargs=requestslib_kwargs)

    def list_launches(self, launched_at_min=None, launched_at_max=None,
                      instance=None, requestslib_kwargs=None):
        """
        @summary: Retrieves launch events details filtered by minimum date,
            maximum date or both with an optional instance
        @param launched_at_min: A string formatted as
            YYYY-MM-DD HH:MM:SS.mmmmmm
        @type launched_at_min: String
        @param launched_at_max: A string formatted as
            YYYY-MM-DD HH:MM:SS.mmmmmm
        @type launched_at_max: String
        @param instance: The uuid of the server
        @type instance: String
        @return: Dictionary, key:'launches' with value: an unordered list of
            launch events starting at launched_at_min and ending at
            launched_at_max
        @rtype:  ServerLaunches Object
        @note: depending on the existence of the params, different GETs
            will be executed

            GET
            /db/usage/launches/

            GET
            /db/usage/launches/?instance={uuid}
            (also works with any combination of below params)

            GET
            /db/usage/launches/?launched_at_min={launched_at_min}
                &launched_at_max={launched_at_max}

            GET
            /db/usage/launches/?launched_at_min={launched_at_min}

            GET
            /db/usage/launches/?launched_at_max={launched_at_max}
        """
        if launched_at_min and launched_at_max:
            params = {'launched_at_min': launched_at_min,
                      'launched_at_max': launched_at_max}
        elif launched_at_max:
            params = {'launched_at_max': launched_at_max}
        elif launched_at_min:
            params = {'launched_at_min': launched_at_min}
        else:
            params = {}

        if instance:
            params['instance'] = instance

        url = "{0}{1}".format(self.url, '/db/usage/launches/')
        return self.request('GET', url, params=params,
                            response_entity_type=ServerLaunches,
                            requestslib_kwargs=requestslib_kwargs)

    def list_deletes(self, deleted_at_min=None, deleted_at_max=None,
                     instance=None, requestslib_kwargs=None):
        """
        @summary: Retrieves delete events details filtered by minimum date,
            maximum date or both with an optional instance
        @param deleted_at_min: A string formatted as
            YYYY-MM-DD HH:MM:SS.mmmmmm
        @type deleted_at_min: String
        @param deleted_at_max: A string formatted as
            YYYY-MM-DD HH:MM:SS.mmmmmm
        @type deleted_at_max: String
        @param instance: The uuid of the server
        @type instance: String
        @return: Dictionary, key:'deletes' with value: an unordered list of
            delete events starting at deleted_at_min and ending at
            deleted_at_max
        @rtype:  ServerDeletes Object
        @note: depending on the existence of the param different GETs
            will be executed

            GET
            /db/usage/deletes/

            GET
            /db/usage/deletes/?instance={uuid}
            (also works with any combination of below params)

            GET
            /db/usage/deletes/?deleted_at_min={deleted_at_min}
                &deleted_at_max={deleted_at_max}

            GET
            /db/usage/deletes/?deleted_at_min={deleted_at_min}

            GET
            /db/usage/deletes/?deleted_at_max={deleted_at_max}
        """
        if deleted_at_min and deleted_at_max:
            params = {'deleted_at_min': deleted_at_min,
                      'deleted_at_max': deleted_at_max}
        elif deleted_at_min:
            params = {'deleted_at_min': deleted_at_min}
        elif deleted_at_max:
            params = {'deleted_at_min': deleted_at_max}
        else:
            params = {}

        if instance:
            params['instance'] = instance

        url = "{0}{1}".format(self.url, '/db/usage/deletes/')
        return self.request('GET', url, params=params,
                            response_entity_type=ServerDeletes,
                            requestslib_kwargs=requestslib_kwargs)

    def list_image_exists(self):
        """
        @summary: Retrieves the latest exists events for all images.
        @return: Dictionary key:'exists' with value as a list of exists events
        @rtype:  ImageExists Object
            GET
            /db/usage/glance/exists/
        """
        url = "{0}{1}".format(self.url, '/db/usage/glance/exists/')
        return self.request('GET', url, response_entity_type=ImageExists)

    def list_images(self):
        """
        @summary: Retrieves image usage events details.
        @return: Dictionary, key:'images' with value: an unordered list of
            image usage events.
        @rtype:  ImageUsages Object

            GET
            /db/usage/glance/images/
        """
        url = "{0}{1}".format(self.url, '/db/usage/glance/images/')
        return self.request('GET', url, response_entity_type=ImageUsages)

    def list_image_deletes(self):
        """
        @summary: Retrieves image delete events details.
        @return: Dictionary, key:'deletes' with value: an unordered list of
            image delete events.
        @rtype:  ImageDeletes Object

            GET
            /db/usage/glance/deletes/
        """
        url = "{0}{1}".format(self.url, '/db/usage/glance/deletes/')
        return self.request('GET', url, response_entity_type=ImageDeletes)
