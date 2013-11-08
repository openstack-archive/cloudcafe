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
from cloudcafe.images.v2.models.image import \
    Image, Images, ImagePatch, Member, Members


class ImagesClient(AutoMarshallingRestClient):
    """@summary: Client for Images v2"""

    def __init__(self, base_url, auth_token, serialize_format,
                  deserialize_format):
        """@summary: Constructs the images api client"""

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

    def get_images_schema(self, requestslib_kwargs=None):
        """
            Get JSON-schema of the images object.
        """
        url = '{0}{1}'.format(self.base_url, '/schemas/images')
        return self.request('GET', url, requestslib_kwargs=requestslib_kwargs)

    def get_image_schema(self, requestslib_kwargs=None):
        """
            Get JSON-schema of the image object.
        """
        url = '{0}{1}'.format(self.base_url, '/schemas/image')
        return self.request('GET', url, requestslib_kwargs=requestslib_kwargs)

    def create_image(self, id_=None, name=None, visibility=None,
                     status=None, protected=None, tags=None, checksum=None,
                     size=None, created_at=None, updated_at=None, file_=None,
                     self_=None, schema=None, container_format=None,
                     disk_format=None, min_disk=None, min_ram=None,
                     kernel_id=None, ramdisk_id=None, requestslib_kwargs=None):
        """
            Create a new Image.
        """
        image = Image(id_=id_, name=name, visibility=visibility,
                      status=status, protected=protected, tags=tags,
                      checksum=checksum, size=size, created_at=created_at,
                      updated_at=updated_at, file_=file_, self_=self_,
                      schema=schema, container_format=container_format,
                      disk_format=disk_format, min_disk=min_disk,
                      min_ram=min_ram, kernel_id=kernel_id,
                      ramdisk_id=ramdisk_id)
        url = '{0}/images'.format(self.base_url)

        return self.request('POST', url, request_entity=image,
                            response_entity_type=Image,
                            requestslib_kwargs=requestslib_kwargs)

    def update_image(self, image_id, replace=None, add=None, remove=None,
                     requestslib_kwargs=None):
        """
            Update an Image.
            @param add a dictionary of properties to be added,
            @param replace a dictionary of properties to be replaced,
            @param remove a list of properties to be removed
        """
        url = '{0}/images/{1}'.format(self.base_url, image_id)

        image_patch = ImagePatch(add, replace, remove)
        headers = self.default_headers
        headers['Content-Type'] = (
            'application/openstack-images-v2.0-json-patch')

        return self.request('PATCH', url,
                            headers=headers,
                            request_entity=image_patch,
                            response_entity_type=Image,
                            requestslib_kwargs=requestslib_kwargs)

    def add_tag(self, image_id, tag, requestslib_kwargs=None):
        url = '{base_url}/images/{image_id}/tags/{tag}'.format(
            base_url=self.base_url, image_id=image_id, tag=tag)

        return self.request('PUT', url,
                            requestslib_kwargs=requestslib_kwargs)

    def list_members(self, image_id):
        url = '{base_url}/images/{image_id}/members'.format(
            base_url=self.base_url, image_id=image_id)

        return self.request('GET', url, response_entity_type=Members)

    def delete_tag(self, image_id, tag, requestslib_kwargs=None):
        url = '{base_url}/images/{image_id}/tags/{tag}'.format(
            base_url=self.base_url, image_id=image_id, tag=tag)

        return self.request('DELETE', url,
                            requestslib_kwargs=requestslib_kwargs)

    def add_member(self, image_id, member_id, requestslib_kwargs=None):
        url = '{base_url}/images/{image_id}/members'.format(
            base_url=self.base_url, image_id=image_id)

        member = Member(image_id=image_id, member_id=member_id)

        return self.request('POST', url,
                            request_entity=member,
                            response_entity_type=Member,
                            requestslib_kwargs=requestslib_kwargs)

    def update_member(self, image_id, member_id, status,
                      requestslib_kwargs=None):
        url = '{base_url}/images/{image_id}/members/{member_id}'.format(
            base_url=self.base_url, image_id=image_id, member_id=member_id)

        member = Member(image_id=image_id, member_id=member_id, status=status)

        return self.request('PUT', url,
                            request_entity=member,
                            response_entity_type=Member,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_member(self, image_id, member_id):
        url = '{base_url}/images/{image_id}/members/{member_id}'.format(
            base_url=self.base_url, image_id=image_id, member_id=member_id)

        return self.request('DELETE', url)

    def list_images(self, name=None, disk_format=None, container_format=None,
                    visibility=None, status=None, checksum=None, owner=None,
                    min_ram=None, min_disk=None, changes_since=None,
                    protected=None, size_min=None, size_max=None,
                    sort_key=None, sort_dir=None, marker=None, limit=None,
                    requestslib_kwargs=None, **param_kwargs):
        """
        @summary: List all details for all available images.
        @param name: Image Name
        @type name: String
        @param disk_format: Disk_format
        @type disk_format: String
        @param container_format: Container_format
        @type container_format: String
        @param visibility: Image Visibility
        @type visibility: String
        @param status: Image Status
        @type status: String
        @param checksum: Image Checksum
        @type checksum: String
        @param owner: Image Owner
        @type owner: String
        @param min_ram: Value of the minimum ram of the image in bytes
        @type min_ram: String
        @param min_disk: Value of the minimum disk of the image in bytes
        @type min_disk: String
        @param changes_since: changed since the changes-since time
        @type changes_since: DateTime
        @param protected: 0|1
        @type protected: int
        @param size_min: Value of the minimum size of the image in bytes
        @type size_min: String
        @param size_max: Value of the maximum size of the image in bytes
        @type size_max: String
        @param sort_key: Sort Key. Default is 'created_at'
        @type sort_key: String
        @param sort_dir: Sort Direction. Default is 'desc'
        @type sort_dir: String
        @param marker: The ID of the last item in the previous list
        @type marker: String
        @param limit: Sets the page size.
        @type limit: int
        @param param_kwargs: dynamic image properties as filter params
        @type param_kwargs: Dictionary
        @return: lists all images visible by the account filtered by the params
        @rtype: Response with Image List as response.entity
        """
        url = '{base_url}/images'.format(base_url=self.base_url)

        params = {'name': name, 'disk_format': disk_format, 'status': status,
                  'container_format': container_format, 'checksum': checksum,
                  'visibility': visibility, 'owner': owner, 'min_ram': min_ram,
                  'min_disk': min_disk, 'changes_since': changes_since,
                  'protected': protected, 'size_min': size_min,
                  'size_max': size_max, 'marker': marker, 'sort_key': sort_key,
                  'sort_dir': sort_dir, 'limit': limit}

        params.update(param_kwargs)
        return self.request('GET', url, params=params,
                            response_entity_type=Images,
                            requestslib_kwargs=requestslib_kwargs)

    def get_image(self, image_id, requestslib_kwargs=None):
        url = '{0}/images/{1}'.format(self.base_url, image_id)
        return self.request('GET', url, response_entity_type=Image,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_image(self, image_id, requestslib_kwargs=None):
        url = '{0}/images/{1}'.format(self.base_url, image_id)
        return self.request('DELETE', url,
                            requestslib_kwargs=requestslib_kwargs)

    def store_raw_image_data(self, image_id, image_data,
                             requestslib_kwargs=None):
        url = '{0}/images/{1}/file'.format(self.base_url, image_id)
        headers = {'Content-Type': 'application/octet-stream'}
        return self.request('PUT', url, headers=headers, data=image_data)

    def get_raw_image_data(self, image_id, requestslib_kwargs=None):
        raise NotImplementedError
