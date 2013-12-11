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
from cloudcafe.common.resources import ResourcePool
from cloudcafe.common.tools.datagen import rand_name
from cloudcafe.images.common.types import \
    ImageContainerFormat, ImageDiskFormat


class ImagesBehaviors(BaseBehavior):
    """@summary: Behaviors class for images v2"""

    def __init__(self, images_client, images_config):
        super(ImagesBehaviors, self).__init__()
        self.config = images_config
        self.client = images_client
        self.resources = ResourcePool()

    def create_new_image(self, container_format=None, disk_format=None,
                         name=None, protected=None, tags=None,
                         visibility=None):
        """@summary: Create new image and add it for deletion"""

        if container_format is None:
            container_format = ImageContainerFormat.BARE
        if disk_format is None:
            disk_format = ImageDiskFormat.RAW
        if name is None:
            name = rand_name('image')

        response = self.client.create_image(
            container_format=container_format, disk_format=disk_format,
            name=name, protected=protected, tags=tags, visibility=visibility)
        image = response.entity
        if image is not None:
            self.resources.add(image.id_, self.client.delete_image)
        return image

    def create_new_images(self, container_format=None, disk_format=None,
                          name=None, protected=None, tags=None,
                          visibility=None, count=1):
        """@summary: Create new images and add them for deletion"""

        image_list = []
        for i in range(count):
            image = self.create_new_image(
                container_format=container_format, disk_format=disk_format,
                name=name, protected=protected, tags=tags,
                visibility=visibility)
            image_list.append(image)
        return image_list

    def list_images_pagination(self, name=None, disk_format=None,
                               container_format=None, visibility=None,
                               status=None, checksum=None, owner=None,
                               min_ram=None, min_disk=None, changes_since=None,
                               protected=None, size_min=None, size_max=None,
                               sort_key=None, sort_dir=None, marker=None,
                               limit=None):
        """@summary: Get images accounting for pagination as needed"""

        image_list = []
        results_limit = self.config.results_limit
        response = self.client.list_images(
            name=name, disk_format=disk_format,
            container_format=container_format, visibility=visibility,
            status=status, checksum=checksum, owner=owner, min_ram=min_ram,
            min_disk=min_disk, changes_since=changes_since,
            protected=protected, size_min=size_min, size_max=size_max,
            sort_key=sort_key, sort_dir=sort_dir, marker=marker, limit=limit)
        images = response.entity
        while len(images) == results_limit:
            image_list += images
            marker = images[results_limit - 1].id_
            response = self.client.list_images(
                name=name, disk_format=disk_format,
                container_format=container_format, visibility=visibility,
                status=status, checksum=checksum, owner=owner, min_ram=min_ram,
                min_disk=min_disk, changes_since=changes_since,
                protected=protected, size_min=size_min, size_max=size_max,
                sort_key=sort_key, sort_dir=sort_dir, marker=marker,
                limit=limit)
            images = response.entity
        image_list += images
        return image_list

    def get_member_ids(self, image_id):
        """
        @summary: Return a complete list of ids for all members for a given
        image id
        """

        response = self.client.list_members(image_id)
        members = response.entity
        return [member.member_id for member in members]
