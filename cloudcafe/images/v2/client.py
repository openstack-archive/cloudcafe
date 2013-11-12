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
        """@summary: Get json schema of the images object"""

        url = '{0}{1}'.format(self.base_url, '/schemas/images')
        return self.request('GET', url, requestslib_kwargs=requestslib_kwargs)

    def get_image_schema(self, requestslib_kwargs=None):
        """@summary: Get json schema of the image object"""

        url = '{0}{1}'.format(self.base_url, '/schemas/image')
        return self.request('GET', url, requestslib_kwargs=requestslib_kwargs)

    def create_image(self, checksum=None, container_format=None,
                       created_at=None, disk_format=None, file=None, id=None,
                       min_disk=None, min_ram=None, name=None, protected=None,
                       schema=None, self_=None, size=None, status=None,
                       tags=None, updated_at=None, visibility=None,
                       additional_properties=None, requestslib_kwargs=None):
        """@summary:  Create a new image"""

        image = Image(checksum=checksum, container_format=container_format,
                      created_at=created_at, disk_format=disk_format,
                      file=file, id=id, min_disk=min_disk, min_ram=min_ram,
                      name=name, protected=protected, schema=schema,
                      self_=self_, size=size, status=status, tags=tags,
                      updated_at=updated_at, visibility=visibility,
                      additional_properties=additional_properties)
        url = '{0}/images'.format(self.base_url)
        return self.request('POST', url, request_entity=image,
                            response_entity_type=Image,
                            requestslib_kwargs=requestslib_kwargs)

    def get_image(self, image_id, requestslib_kwargs=None):
        """@summary: Get a single image"""

        url = '{0}/images/{1}'.format(self.base_url, image_id)
        return self.request('GET', url, response_entity_type=Image,
                            requestslib_kwargs=requestslib_kwargs)

    def list_images(self, name=None, disk_format=None, container_format=None,
                      visibility=None, status=None, checksum=None, owner=None,
                      min_ram=None, min_disk=None, changes_since=None,
                      protected=None, size_min=None, size_max=None,
                      sort_key=None, sort_dir=None, marker=None, limit=None,
                      requestslib_kwargs=None, **param_kwargs):
        """@summary: List all images"""

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

    def update_image(self, image_id, replace=None, add=None, remove=None,
                       requestslib_kwargs=None):
        """@summary: Update an existing image"""

        url = '{0}/images/{1}'.format(self.base_url, image_id)
        image_patch = ImagePatch(add, replace, remove)
        headers = self.default_headers
        headers['Content-Type'] = (
            'application/openstack-images-v2.0-json-patch')
        return self.request('PATCH', url, headers=headers,
                            request_entity=image_patch,
                            response_entity_type=Image,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_image(self, image_id, requestslib_kwargs=None):
        """@summary: Delete an image"""

        url = '{0}/images/{1}'.format(self.base_url, image_id)
        return self.request('DELETE', url,
                            requestslib_kwargs=requestslib_kwargs)

    def store_raw_image_data(self, image_id, image_data,
                                requestslib_kwargs=None):
        """@summary: Upload image data"""

        url = '{0}/images/{1}/file'.format(self.base_url, image_id)
        headers = {'Content-Type': 'application/octet-stream'}
        return self.request('PUT', url, headers=headers, data=image_data)

    def get_raw_image_data(self, image_id, requestslib_kwargs=None):
        """@summary: Get image data"""

        raise NotImplementedError

    def add_tag(self, image_id, tag, requestslib_kwargs=None):
        """@summary: Add a tag to an image"""

        url = '{base_url}/images/{image_id}/tags/{tag}'.format(
            base_url=self.base_url, image_id=image_id, tag=tag)
        return self.request('PUT', url,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_tag(self, image_id, tag, requestslib_kwargs=None):
        """@summary: Delete a tag from an image"""

        url = '{base_url}/images/{image_id}/tags/{tag}'.format(
            base_url=self.base_url, image_id=image_id, tag=tag)
        return self.request('DELETE', url,
                            requestslib_kwargs=requestslib_kwargs)

    def get_image_members_schema(self, requestslib_kwargs=None):
        """@summary: Get schema of the image members object"""

        url = '{0}{1}'.format(self.base_url, '/schemas/members')
        return self.request('GET', url, requestslib_kwargs=requestslib_kwargs)

    def get_image_member_schema(self, requestslib_kwargs=None):
        """@summary: Get schema of the image member object"""

        url = '{0}{1}'.format(self.base_url, '/schemas/member')
        return self.request('GET', url, requestslib_kwargs=requestslib_kwargs)

    def add_member(self, image_id, member_id, requestslib_kwargs=None):
        """@summary: Add a member to an image"""

        url = '{base_url}/images/{image_id}/members'.format(
            base_url=self.base_url, image_id=image_id)
        member = Member(image_id=image_id, member_id=member_id)
        return self.request('POST', url, request_entity=member,
                            response_entity_type=Member,
                            requestslib_kwargs=requestslib_kwargs)

    def list_members(self, image_id):
        """@summary: List all image members"""

        url = '{base_url}/images/{image_id}/members'.format(
            base_url=self.base_url, image_id=image_id)
        return self.request('GET', url, response_entity_type=Members)

    def update_member(self, image_id, member_id, status,
                        requestslib_kwargs=None):
        """@summary: Update a member for an image"""

        url = '{base_url}/images/{image_id}/members/{member_id}'.format(
            base_url=self.base_url, image_id=image_id, member_id=member_id)
        member = Member(image_id=image_id, member_id=member_id, status=status)
        return self.request('PUT', url, request_entity=member,
                            response_entity_type=Member,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_member(self, image_id, member_id):
        """@summary: Delete a member from an image"""

        url = '{base_url}/images/{image_id}/members/{member_id}'.format(
            base_url=self.base_url, image_id=image_id, member_id=member_id)
        return self.request('DELETE', url)

    def get_tasks_schema(self, requestslib_kwargs=None):
        """@summary: Get schema of the tasks object"""

        url = '{0}{1}'.format(self.base_url, '/schemas/tasks')
        return self.request('GET', url, requestslib_kwargs=requestslib_kwargs)

    def get_task_schema(self, requestslib_kwargs=None):
        """@summary: Get schema of the task object"""

        url = '{0}{1}'.format(self.base_url, '/schemas/task')
        return self.request('GET', url, requestslib_kwargs=requestslib_kwargs)
