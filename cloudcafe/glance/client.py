"""
Copyright 2015 Rackspace

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

from cloudcafe.glance.models.image import (
    Image, Images, ImageUpdate, Member, Members)
from cloudcafe.glance.models.task import Task, Tasks
from cloudcafe.glance.models.versions import Versions


class ImagesClient(AutoMarshallingHTTPClient):
    """@summary: Client for Images"""

    def __init__(self, base_url, auth_token, serialize_format,
                 deserialize_format):
        """@summary: Constructs the Images API client"""

        super(ImagesClient, self).__init__(serialize_format,
                                           deserialize_format)
        self.auth_token = auth_token
        self.serialize_format = serialize_format
        self.deserialize_format = deserialize_format
        self.default_headers['X-Auth-Token'] = auth_token
        ct = ''.join(['application/', self.serialize_format])
        accept = ''.join(['application/', self.deserialize_format])
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept
        self.base_url = base_url

    def list_images(self, params=None, requestslib_kwargs=None):
        """
        @summary: List all images

        @param params: Parameters to alter the returned list of images
        @type params: Dictionary
        @param requestslib_kwargs: Keyword arguments to be passed on to
                                   python requests
        @type requestslib_kwargs: Dictionary

        @return: Response object
        @rtype: Object
        """

        url = '{0}/images'.format(self.base_url)

        return self.request('GET', url, params=params,
                            response_entity_type=Images,
                            requestslib_kwargs=requestslib_kwargs)

    def get_image_details(self, image_id, requestslib_kwargs=None):
        """
        @summary: Get the details of an image

        @param image_id: Id of image to be returned
        @type params: UUID
        @param requestslib_kwargs: Keyword arguments to be passed on to
                                   python requests
        @type requestslib_kwargs: Dictionary

        @return: Response object
        @rtype: Object
        """

        url = '{0}/images/{1}'.format(self.base_url, image_id)

        return self.request('GET', url, response_entity_type=Image,
                            requestslib_kwargs=requestslib_kwargs)

    def register_image(self, checksum=None, container_format=None,
                       created_at=None, disk_format=None, file_=None, id_=None,
                       min_disk=None, min_ram=None, name=None, protected=None,
                       schema=None, self_=None, size=None, status=None,
                       tags=None, updated_at=None, visibility=None,
                       additional_properties=None, requestslib_kwargs=None):
        """
        @summary:  Register an image - Not listed in the Images API docs

        @param checksum: Checksum for the image being created
        @type checksum: String
        @param container_format: Container format for the image being created
        @type container_format: String
        @param created_at: Created at for the image being created
        @type created_at: Datetime
        @param disk_format: Disk format for the image being created
        @type disk_format: String
        @param file_: File location for the image being created
        @type file_: String
        @param id_: Id for the image being created
        @type id_: UUID
        @param min_disk: Minimum disk for the image being created
        @type min_disk: String
        @param min_ram: Minimum ram for the image being created
        @type min_ram: String
        @param name: Name for the image being created
        @type name: String
        @param protected: Protected flag for the image being created
        @type protected: Boolean
        @param schema: Schema for the image being created
        @type schema: String
        @param self_: Self location for the image being created
        @type self_: String
        @param size: Size for the image being created
        @type size: String
        @param status: Status for the image being created
        @type status: String
        @param tags: Tags for the image being created
        @type tags: Dictionary
        @param updated_at: Updated at for the image being created
        @type updated_at: Datetime
        @param visibility: Visibility for the image being created
        @type visibility: String
        @param additional_properties: Additional properties for the image being
                                      created
        @type additional_properties: Dictionary
        @param requestslib_kwargs: Keyword arguments to be passed on to
                                   python requests
        @type requestslib_kwargs: Dictionary


        @return: Response object
        @rtype: Object
        """

        url = '{0}/images'.format(self.base_url)
        image = Image(checksum=checksum, container_format=container_format,
                      created_at=created_at, disk_format=disk_format,
                      file_=file_, id_=id_, min_disk=min_disk, min_ram=min_ram,
                      name=name, protected=protected, schema=schema,
                      self_=self_, size=size, status=status, tags=tags,
                      updated_at=updated_at, visibility=visibility,
                      additional_properties=additional_properties)

        return self.request('POST', url, request_entity=image,
                            response_entity_type=Image,
                            requestslib_kwargs=requestslib_kwargs)

    def store_image_file(self, image_id, file_data, content_type=None,
                         requestslib_kwargs=None):
        """
        @summary: Store an image file data - Not listed in the Images API docs

        @param image_id: Id of image to store image file data to
        @type image_id: UUID
        @param file_data: File date to be stored to the image
        @type file_data: Data
        @param content_type: Content type of data to be stored to the image
        @type content_type: String
        @param requestslib_kwargs: Keyword arguments to be passed on to
                                   python requests
        @type requestslib_kwargs: Dictionary

        @return: Response object
        @rtype: Object
        """

        url = '{0}/images/{1}/file'.format(self.base_url, image_id)
        content_type = content_type or 'application/octet-stream'
        headers = {'Content-Type': content_type}

        return self.request('PUT', url, headers=headers, data=file_data)

    def get_image_file(self, image_id, requestslib_kwargs=None):
        """
        @summary: Get an image file data - Not listed in the Images API docs

        @param image_id: Id of image to return image file data from
        @type image_id: UUID
        @param requestslib_kwargs: Keyword arguments to be passed on to
                                   python requests
        @type requestslib_kwargs: Dictionary

        @return: Response object
        @rtype: Object
        """

        url = '{0}/images/{1}/file'.format(self.base_url, image_id)

        return self.request('GET', url, response_entity_type=Image,
                            requestslib_kwargs=requestslib_kwargs)

    def update_image(self, image_id, replace=None, add=None, remove=None,
                     requestslib_kwargs=None):
        """
        @summary: Update an image

        @param image_id: Id of image to update
        @type image_id: UUID
        @param replace: Image operation to replace an attribute of an image
                        including the actual value to replace
        @type replace: Dictionary
        @param add: Image operation to add an attribute to an image including
                    the actual value to add
        @type add: Dictionary
        @param remove: Image operation to remove an attribute from an image
                       including the actual value to remove
        @param requestslib_kwargs: Keyword arguments to be passed on to
                                   python requests
        @type requestslib_kwargs: Dictionary

        @return: Response object
        @rtype: Object
        """

        url = '{0}/images/{1}'.format(self.base_url, image_id)
        image_update = ImageUpdate(add, replace, remove)
        headers = self.default_headers
        headers['Content-Type'] = (
            'application/openstack-images-v2.0-json-patch')

        return self.request('PATCH', url, headers=headers,
                            request_entity=image_update,
                            response_entity_type=Image,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_image(self, image_id, requestslib_kwargs=None):
        """
        @summary: Delete an image

        @param image_id: Id of image to delete
        @type image_id: UUID
        @param requestslib_kwargs: Keyword arguments to be passed on to
                                   python requests
        @type requestslib_kwargs: Dictionary

        @return: Response object
        @rtype: Object
        """

        url = '{0}/images/{1}'.format(self.base_url, image_id)

        return self.request('DELETE', url,
                            requestslib_kwargs=requestslib_kwargs)

    def list_image_members(self, image_id, params=None,
                           requestslib_kwargs=None):
        """
        @summary: List all image members

        @param image_id: Id of image to list image members for
        @type image_id: UUID
        @param params: Parameters to alter the returned list of images
        @type params: Dictionary
        @param requestslib_kwargs: Keyword arguments to be passed on to
                                   python requests
        @type requestslib_kwargs: Dictionary

        @return: Response object
        @rtype: Object
        """

        url = '{0}/images/{1}/members'.format(self.base_url, image_id)

        return self.request('GET', url, params=params,
                            response_entity_type=Members,
                            requestslib_kwargs=requestslib_kwargs)

    def get_image_member(self, image_id, member_id, requestslib_kwargs=None):
        """
        @summary: Get an image member of an image

        @param image_id: Id of image to use to get image member id
        @type image_id: UUID
        @param member_id: Id of image member to return
        @type member_id: String
        @param requestslib_kwargs: Keyword arguments to be passed on to
                                   python requests
        @type requestslib_kwargs: Dictionary

        @return: Response object
        @rtype: Object
        """

        url = '{0}/images/{1}/members/{2}'.format(self.base_url, image_id,
                                                  member_id)

        return self.request('GET', url, response_entity_type=Member,
                            requestslib_kwargs=requestslib_kwargs)

    def create_image_member(self, image_id, member_id,
                            requestslib_kwargs=None):
        """
        @summary: Create an image member

        @param image_id: Id of image to add image member id to
        @type image_id: UUID
        @param member_id: Id of image member to add to the image
        @type member_id: String
        @param requestslib_kwargs: Keyword arguments to be passed on to
                                   python requests
        @type requestslib_kwargs: Dictionary

        @return: Response object
        @rtype: Object
        """

        url = '{0}/images/{1}/members'.format(self.base_url, image_id)
        member = Member(member_id=member_id)

        return self.request('POST', url, request_entity=member,
                            response_entity_type=Member,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_image_member(self, image_id, member_id,
                            requestslib_kwargs=None):
        """
        @summary: Delete an image member

        @param image_id: Id of image to delete image member id from
        @type image_id: UUID
        @param member_id: Id of image member to delete from the image
        @type member_id: String
        @param requestslib_kwargs: Keyword arguments to be passed on to
                                   python requests
        @type requestslib_kwargs: Dictionary

        @return: Response object
        @rtype: Object
        """

        url = '{0}/images/{1}/members/{2}'.format(self.base_url, image_id,
                                                  member_id)

        return self.request('DELETE', url,
                            requestslib_kwargs=requestslib_kwargs)

    def update_image_member(self, image_id, member_id, status,
                            requestslib_kwargs=None):
        """@summary: Update an image member

        @param image_id: Id of image to update the image member id of
        @type image_id: UUID
        @param member_id: Id of image member to update from the image
        @type member_id: String
        @param status: Status to which the image member should be set
        @type status: String
        @param requestslib_kwargs: Keyword arguments to be passed on to
                                   python requests
        @type requestslib_kwargs: Dictionary

        @return: Response object
        @rtype: Object
        """

        url = '{0}/images/{1}/members/{2}'.format(self.base_url, image_id,
                                                  member_id)
        member = Member(status=status)

        return self.request('PUT', url, request_entity=member,
                            response_entity_type=Member,
                            requestslib_kwargs=requestslib_kwargs)

    def add_image_tag(self, image_id, tag, requestslib_kwargs=None):
        """
        @summary: Add an image tag

        @param image_id: Id of image to add image tag to
        @type image_id: UUID
        @param tag: Image tag to add to the image
        @type tag: String
        @param requestslib_kwargs: Keyword arguments to be passed on to
                                   python requests
        @type requestslib_kwargs: Dictionary

        @return: Response object
        @rtype: Object
        """

        url = '{0}/images/{1}/tags/{2}'.format(self.base_url, image_id, tag)

        return self.request('PUT', url, requestslib_kwargs=requestslib_kwargs)

    def delete_image_tag(self, image_id, tag, requestslib_kwargs=None):
        """
        @summary: Delete an image tag

        @param image_id: Id of image to delete image tag from
        @type image_id: UUID
        @param tag: Image tag to delete from the image
        @type tag: String
        @param requestslib_kwargs: Keyword arguments to be passed on to
                                   python requests
        @type requestslib_kwargs: Dictionary

        @return: Response object
        @rtype: Object
        """

        url = '{0}/images/{1}/tags/{2}'.format(self.base_url, image_id, tag)

        return self.request('DELETE', url,
                            requestslib_kwargs=requestslib_kwargs)

    def list_tasks(self, requestslib_kwargs=None):
        """
        @summary: List all tasks

        @param requestslib_kwargs: Keyword arguments to be passed on to
                                   python requests
        @type requestslib_kwargs: Dictionary

        @return: Response object
        @rtype: Object
        """

        url = '{0}/tasks'.format(self.base_url)

        return self.request('GET', url, response_entity_type=Tasks,
                            requestslib_kwargs=requestslib_kwargs)

    def get_task_details(self, task_id, requestslib_kwargs=None):
        """
        @summary: Get the details of a task

        @param task_id: Id of the task being returned
        @type task_id: UUID
        @param requestslib_kwargs: Keyword arguments to be passed on to
                                   python requests
        @type requestslib_kwargs: Dictionary

        @return: Response object
        @rtype: Object
        """

        url = '{0}/tasks/{1}'.format(self.base_url, task_id)

        return self.request('GET', url, response_entity_type=Task,
                            requestslib_kwargs=requestslib_kwargs)

    def task_to_import_image(self, input_=None, type_=None,
                             requestslib_kwargs=None):
        """
        @summary: Create a task to import an image

        @param input_: Container for import input parameters containing
                       image properties and import from
        @type input_: Dictionary
        @param type_: Type of task
        @type type_: String
        @param requestslib_kwargs: Keyword arguments to be passed on to
                                   python requests
        @type requestslib_kwargs: Dictionary

        @return: Response object
        @rtype: Object
        """

        url = '{0}/tasks'.format(self.base_url)
        task = Task(input_=input_, type_=type_)

        return self.request('POST', url, request_entity=task,
                            response_entity_type=Task,
                            requestslib_kwargs=requestslib_kwargs)

    def task_to_export_image(self, input_=None, type_=None,
                             requestslib_kwargs=None):
        """
        @summary: Create a task to export an image

        @param input_: Container for export input parameters containing
                       image uuid and receiving swift container
        @type input_: Dictionary
        @param type_: Type of task
        @type type_: String
        @param requestslib_kwargs: Keyword arguments to be passed on to
                                   python requests
        @type requestslib_kwargs: Dictionary

        @return: Response object
        @rtype: Object
        """

        url = '{0}/tasks'.format(self.base_url)
        task = Task(input_=input_, type_=type_)

        return self.request('POST', url, request_entity=task,
                            response_entity_type=Task,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_task(self, task_id, requestslib_kwargs=None):
        """
        @summary: Delete a task - Not listed in the Images API docs

        @param task_id: Id of the task being deleted
        @type task_id: UUID
        @param requestslib_kwargs: Keyword arguments to be passed on to
                                   python requests
        @type requestslib_kwargs: Dictionary

        @return: Response object
        @rtype: Object
        """

        url = '{0}/tasks/{1}'.format(self.base_url, task_id)

        return self.request('DELETE', url, response_entity_type=Task,
                            requestslib_kwargs=requestslib_kwargs)

    def get_images_schema(self, requestslib_kwargs=None):
        """
        @summary: Get images json schema

        @param requestslib_kwargs: Keyword arguments to be passed on to
                                   python requests
        @type requestslib_kwargs: Dictionary

        @return: Response object
        @rtype: Object
        """

        url = '{0}/{1}'.format(self.base_url, 'schemas/images')

        return self.request('GET', url, requestslib_kwargs=requestslib_kwargs)

    def get_image_schema(self, requestslib_kwargs=None):
        """
        @summary: Get image json schema

        @param requestslib_kwargs: Keyword arguments to be passed on to
                                   python requests
        @type requestslib_kwargs: Dictionary

        @return: Response object
        @rtype: Object
        """

        url = '{0}/{1}'.format(self.base_url, 'schemas/image')

        return self.request('GET', url, requestslib_kwargs=requestslib_kwargs)

    def get_image_members_schema(self, requestslib_kwargs=None):
        """
        @summary: Get image members schema

        @param requestslib_kwargs: Keyword arguments to be passed on to
                                   python requests
        @type requestslib_kwargs: Dictionary

        @return: Response object
        @rtype: Object
        """

        url = '{0}/{1}'.format(self.base_url, 'schemas/members')

        return self.request('GET', url, requestslib_kwargs=requestslib_kwargs)

    def get_image_member_schema(self, requestslib_kwargs=None):
        """
        @summary: Get image member schema

        @param requestslib_kwargs: Keyword arguments to be passed on to
                                   python requests
        @type requestslib_kwargs: Dictionary

        @return: Response object
        @rtype: Object
        """

        url = '{0}/{1}'.format(self.base_url, 'schemas/member')

        return self.request('GET', url, requestslib_kwargs=requestslib_kwargs)

    def get_tasks_schema(self, requestslib_kwargs=None):
        """
        @summary: Get tasks schema

        @param requestslib_kwargs: Keyword arguments to be passed on to
                                   python requests
        @type requestslib_kwargs: Dictionary

        @return: Response object
        @rtype: Object
        """

        url = '{0}/{1}'.format(self.base_url, 'schemas/tasks')

        return self.request('GET', url, requestslib_kwargs=requestslib_kwargs)

    def get_task_schema(self, requestslib_kwargs=None):
        """
        @summary: Get task schema

        @param requestslib_kwargs: Keyword arguments to be passed on to
                                   python requests
        @type requestslib_kwargs: Dictionary

        @return: Response object
        @rtype: Object
        """

        url = '{0}/{1}'.format(self.base_url, 'schemas/task')

        return self.request('GET', url, requestslib_kwargs=requestslib_kwargs)

    def list_versions(self, url_addition=None, requestslib_kwargs=None):
        """
        @summary: List all versions - Not listed in the Images API docs

        @param url_addition: Additional text to be added to the end of the url
        @type url_addition: String
        @param requestslib_kwargs: Keyword arguments to be passed on to
                                   python requests
        @type requestslib_kwargs: Dictionary

        @return: Response object
        @rtype: Object
        """

        endpoint = self.base_url.replace('/v2', '')
        url = endpoint
        if url_addition:
            url = '{0}{1}'.format(endpoint, url_addition)

        return self.request('GET', url, response_entity_type=Versions,
                            requestslib_kwargs=requestslib_kwargs)
