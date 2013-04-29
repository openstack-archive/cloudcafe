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

from urlparse import urlparse

from cafe.engine.clients.rest import AutoMarshallingRestClient
from cloudcafe.compute.common.models.metadata import Metadata
from cloudcafe.compute.common.models.metadata import MetadataItem
from cloudcafe.compute.images_api.models.image import Image, ImageMin


class ImagesClient(AutoMarshallingRestClient):

    '''
    Client for Image API
    '''

    def __init__(self, url, auth_token, serialize_format, deserialize_format):
        """
        @param url: Base URL for the compute service
        @type url: String
        @param auth_token: Auth token to be used for all requests
        @type auth_token: String
        @param serialize_format: Format for serializing requests
        @type serialize_format: String
        @param deserialize_format: Format for de-serializing responses
        @type deserialize_format: String
        """
        super(ImagesClient, self).__init__(serialize_format,
                                           deserialize_format)
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        ct = ''.join(['application/', self.serialize_format])
        accept = ''.join(['application/', self.deserialize_format])
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept
        self.url = url

    def list_images(self, server_ref=None, image_name=None, status=None,
                    image_type=None, marker=None, changes_since=None,
                    limit=None, requestslib_kwargs=None):

        """
        @summary: Lists IDs, names, and links for all available images.
        @param server_ref: Server id or Url to server
        @type server_ref: String
        @param image_name: Image Name
        @type image_name: String
        @param status: Image Status
        @type status: String
        @param image_type:BASE|SERVER
        @type image_type:String
        @param changes_since: changed since the changes-since time
        @type changes_since: DateTime
        @param marker: The ID of the last item in the previous list
        @type marker: String
        @param limit:Sets the page size.
        @type limit:int
        @return: lists all images visible by the account filtered by the params
        @rtype: Response with Image List as response.entity
        """

        url = '%s/images' % (self.url)

        params = {'server': server_ref, 'name': image_name,
                  'status': status, 'type': image_type, 'marker': marker,
                  'changes-since': changes_since, 'limit': limit}
        return self.request('GET', url, params=params,
                            response_entity_type=ImageMin,
                            requestslib_kwargs=requestslib_kwargs)

    def list_images_with_detail(self, server_ref=None, image_name=None,
                                status=None, image_type=None, marker=None,
                                changes_since=None, limit=None,
                                requestslib_kwargs=None):
        '''
        @summary: List all details for all available images.
        @param server_ref: Server id or Url to server
        @type server_ref: String
        @param image_name: Image Name
        @type image_name: String
        @param status: Image Status
        @type status: String
        @param type:BASE|SERVER
        @type type:String
        @param changes_since: changed since the changes-since time
        @type changes_since: DateTime
        @param marker: The ID of the last item in the previous list
        @type marker: String
        @param limit:Sets the page size.
        @type limit:int
        @return: lists all images visible by the account filtered by the params
        @rtype: Response with Image List as response.entity
        '''

        url = '%s/images/detail' % (self.url)

        params = {'server': server_ref, 'name': image_name,
                  'status': status, 'type': image_type, 'marker': marker,
                  'changes-since': changes_since, 'limit': limit}
        return self.request('GET', url, params=params,
                            response_entity_type=Image,
                            requestslib_kwargs=requestslib_kwargs)

    def get_image(self, image_id, requestslib_kwargs=None):
        '''
        @summary: Lists details of the specified image.
        @param image_id: Image id
        @type image_id: String
        @return: Details of specified Image. BUT no server_id in image details
        @rtype: Response with Image as response.entity
        '''

        url_new = str(image_id)
        url_scheme = urlparse(url_new).scheme
        url = url_new if url_scheme else '%s/images/%s' % (self.url, image_id)

        return self.request('GET', url, response_entity_type=Image,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_image(self, image_id, requestslib_kwargs=None):
        '''
        @summary: Deletes the specified image.
        @param image_id: Image id
        @type image_id: String
        @return: Response code 204 if successful
        @rtype: Response Object
        '''

        url = '%s/images/%s' % (self.url, image_id)
        return self.request('DELETE', url,
                            requestslib_kwargs=requestslib_kwargs)

    def list_image_metadata(self, image_id, requestslib_kwargs=None):
        '''
        @summary: Returns metadata associated with an image
        @param image_id: Image ID
        @type image_id:String
        @return: Metadata associated with an image on success
        @rtype: Response object with metadata dictionary as entity
        '''

        url = '%s/images/%s/metadata' % (self.url, image_id)
        image_response = self.request('GET', url,
                                      response_entity_type=Metadata,
                                      requestslib_kwargs=requestslib_kwargs)
        return image_response

    def set_image_metadata(self, image_id, metadata, requestslib_kwargs=None):
        '''
        @summary: Sets metadata for the specified image
        @param image_id: Image ID
        @type image_id:String
        @param metadata: Metadata to be set for an image
        @type metadata: dictionary
        @return: Metadata associated with an image on success
        @rtype:  Response object with metadata dictionary as entity
        '''

        url = '%s/images/%s/metadata' % (self.url, image_id)
        request_object = Metadata(metadata)
        image_response = self.request('PUT', url,
                                      response_entity_type=Metadata,
                                      request_entity=request_object,
                                      requestslib_kwargs=requestslib_kwargs)
        return image_response

    def update_image_metadata(self, image_id, metadata,
                              requestslib_kwargs=None):
        '''
        @summary: Updates metadata items for the specified image
        @param image_id: Image ID
        @type image_id:String
        @param metadata: Metadata to be updated for an image
        @type metadata: dictionary
        @return: Metadata associated with an image on success
        @rtype:  Response object with metadata dictionary as entity
        '''

        url = '%s/images/%s/metadata' % (self.url, image_id)
        request_object = Metadata(metadata)
        image_response = self.request('POST', url,
                                      response_entity_type=Metadata,
                                      request_entity=request_object,
                                      requestslib_kwargs=requestslib_kwargs)
        return image_response

    def get_image_metadata_item(self, image_id, key, requestslib_kwargs=None):
        '''
        @summary: Retrieves a single metadata item by key
        @param image_id: Image ID
        @type image_id:String
        @param key: Key for which metadata item needs to be retrieved
        @type key: String
        @return: Metadata Item for a key on success
        @rtype:  Response object with metadata dictionary as entity
        '''

        url = '%s/images/%s/metadata/%s' % (self.url, image_id, key)
        image_response = self.request('GET', url,
                                      response_entity_type=MetadataItem,
                                      requestslib_kwargs=requestslib_kwargs)
        return image_response

    def set_image_metadata_item(self, image_id, key, value,
                                requestslib_kwargs=None):
        '''
        @summary: Sets a metadata item for a specified image
        @param image_id: Image ID
        @type image_id:String
        @param key: Key for which metadata item needs to be set
        @type key: String
        @param key: Value which the metadata key needs to be set to
        @type key: String
        @return: Metadata Item for the key on success
        @rtype:  Response object with metadata dictionary as entity
        '''

        url = '%s/images/%s/metadata/%s' % (self.url, image_id, key)
        metadata_item = MetadataItem({key: value})
        image_response = self.request('PUT', url,
                                      response_entity_type=MetadataItem,
                                      request_entity=metadata_item,
                                      requestslib_kwargs=requestslib_kwargs)
        return image_response

    def delete_image_metadata_item(self, image_id, key,
                                   requestslib_kwargs=None):
        '''
        @summary: Sets a metadata item for a specified image
        @param image_id: Image ID
        @type image_id:String
        @param key: Key for which metadata item needs to be set
        @type key: String
        @return: Metadata Item for the key on success
        @rtype:  Response object with metadata dictionary as entity
        '''

        url = '%s/images/%s/metadata/%s' % (self.url, image_id, key)
        image_response = self.request('DELETE', url,
                                      requestslib_kwargs=requestslib_kwargs)
        return image_response
