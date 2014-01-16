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

import calendar
import re
import time

from cafe.engine.behaviors import BaseBehavior
from cloudcafe.common.resources import ResourcePool
from cloudcafe.common.tools.datagen import rand_name
from cloudcafe.images.common.constants import ImageProperties, Messages
from cloudcafe.images.common.exceptions import (
    BuildErrorException, RequiredResourceException, TimeoutException)
from cloudcafe.images.common.types import (
    ImageContainerFormat, ImageDiskFormat, ImageStatus, Schemas, TaskStatus,
    TaskTypes)


class ImagesBehaviors(BaseBehavior):
    """@summary: Behaviors class for images v2"""

    def __init__(self, images_client, images_config):
        super(ImagesBehaviors, self).__init__()
        self.config = images_config
        self.client = images_client
        self.resources = ResourcePool()
        self.error_msg = Messages.ERROR_MSG
        self.id_regex = re.compile(ImageProperties.ID_REGEX)

    def create_new_image(self, image_properties=None, import_from=None,
                         import_from_format=None):
        """
        @summary: Create new image using the create new task method and add it
        for deletion
        """

        if image_properties is None:
            image_properties = {}
        if import_from is None:
            import_from = self.config.import_from
        if import_from_format is None:
            import_from_format = self.config.import_from_format

        input_ = {'image_properties': image_properties,
                  'import_from': import_from,
                  'import_from_format': import_from_format}
        task = self.create_new_task(input_=input_, type_=TaskTypes.IMPORT)
        image_id = task.result.image_id

        response = self.client.get_image(image_id=image_id)
        image = response.entity

        if image is not None:
            self.resources.add(image.id_, self.client.delete_image)

        return image

    def create_new_images(self, image_properties=None, import_from=None,
                          import_from_format=None, count=1):
        """
        @summary: Create new images using the create new task method and add
        them for deletion
        """

        image_list = []

        for i in range(count):
            image = self.create_new_image(
                image_properties=image_properties, import_from=import_from,
                import_from_format=import_from_format)
            image_list.append(image)

        return image_list

    def create_new_image_internal_only(self, container_format=None,
                                       disk_format=None, name=None,
                                       protected=None, tags=None):
        """
        @summary: Create new image via an internal node and add it for
        deletion
        """

        if container_format is None:
            container_format = ImageContainerFormat.BARE
        if disk_format is None:
            disk_format = ImageDiskFormat.RAW
        if name is None:
            name = rand_name('image')

        response = self.client.create_image(
            container_format=container_format, disk_format=disk_format,
            name=name, protected=protected, tags=tags)
        image = response.entity

        if image is not None:
            self.resources.add(image.id_, self.client.delete_image)

        return image

    def create_new_images_internal_only(self, container_format=None,
                                        disk_format=None, name=None,
                                        protected=None, tags=None, count=1):
        """
        @summary: Create new images via an internal node and add them for
        deletion
        """

        image_list = []

        for i in range(count):
            image = self.create_new_image_internal_only(
                container_format=container_format, disk_format=disk_format,
                name=name, protected=protected, tags=tags)
            image_list.append(image)

        return image_list

    def list_images_pagination(self, changes_since=None, checksum=None,
                               container_format=None, disk_format=None,
                               limit=None, marker=None, member_status=None,
                               min_disk=None, min_ram=None, name=None,
                               owner=None, protected=None, size_max=None,
                               size_min=None, sort_dir=None, sort_key=None,
                               status=None, visibility=None):
        """@summary: Get images accounting for pagination as needed"""

        image_list = []
        results_limit = self.config.results_limit
        response = self.client.list_images(
            changes_since=changes_since, checksum=checksum,
            container_format=container_format, disk_format=disk_format,
            limit=limit, marker=marker, member_status=member_status,
            min_disk=min_disk, min_ram=min_ram, name=name, owner=owner,
            protected=protected, size_max=size_max, size_min=size_min,
            sort_dir=sort_dir, sort_key=sort_key, status=status,
            visibility=visibility)
        images = response.entity
        while len(images) == results_limit:
            image_list += images
            marker = images[results_limit - 1].id_
            response = self.client.list_images(
                changes_since=changes_since, checksum=checksum,
                container_format=container_format, disk_format=disk_format,
                limit=limit, marker=marker, member_status=member_status,
                min_disk=min_disk, min_ram=min_ram, name=name, owner=owner,
                protected=protected, size_max=size_max, size_min=size_min,
                sort_dir=sort_dir, sort_key=sort_key, status=status,
                visibility=visibility)
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

    @staticmethod
    def get_creation_delta(image_creation_time_in_sec, time_property):
        """
        @summary: Calculate and return the difference between the image
        creation time and a given image time_property
        """

        time_property_in_sec = calendar.timegm(time_property.timetuple())
        return abs(time_property_in_sec - image_creation_time_in_sec)

    def validate_image(self, image):
        """@summary: Generically validate an image contains crucial expected
        data
        """

        errors = []
        if image.created_at is None:
            errors.append(self.error_msg.format('created_at', not None, None))
        if image.file_ != '/v2/images/{0}/file'.format(image.id_):
            errors.append(self.error_msg.format(
                'file_', '/v2/images/{0}/file'.format(image.id_), image.file_))
        if image.image_type is None:
            errors.append(self.error_msg.format('image_type', not None, None))
        if self.id_regex.match(image.id_) is None:
            errors.append(self.error_msg.format('id_', not None, None))
        if image.min_disk is None:
            errors.append(self.error_msg.format('min_disk', not None, None))
        if image.min_ram is None:
            errors.append(self.error_msg.format('min_ram', not None, None))
        if image.protected is None:
            errors.append(self.error_msg.format('protected', not None, None))
        if image.schema != Schemas.IMAGE_SCHEMA:
            errors.append(self.error_msg.format(
                'schema', Schemas.IMAGE_SCHEMA, image.schema))
        if image.self_ != '/v2/images/{0}'.format(image.id_):
            errors.append(self.error_msg.format(
                'schema', '/v2/images/{0}'.format(image.id_), image.self_))
        if image.status is None:
            errors.append(self.error_msg.format('status', not None, None))
        if image.updated_at is None:
            errors.append(self.error_msg.format('updated_at', not None, None))
        return errors

    def validate_image_member(self, image_id, image_member, member_id):
        """@summary: Generically validate an image member contains crucial
        expected data
        """

        errors = []
        if image_member.created_at is None:
            errors.append(self.error_msg.format('created_at', not None, None))
        if image_member.image_id != image_id:
            errors.append(self.error_msg.format(
                'image_id', image_id, image_member.image_id))
        if image_member.member_id != member_id:
            errors.append(self.error_msg.format(
                'member_id', member_id, image_member.member_id))
        if image_member.schema != Schemas.IMAGE_MEMBER_SCHEMA:
            errors.append(self.error_msg.format(
                'schema', Schemas.IMAGE_MEMBER_SCHEMA, image_member.schema))
        if image_member.status is None:
            errors.append(self.error_msg.format('status', not None, None))
        if image_member.updated_at is None:
            errors.append(self.error_msg.format('updated_at', not None, None))
        return errors

    def wait_for_image_status(self, image_id, desired_status,
                              interval_time=None, timeout=None):
        """
        @summary: Waits for a image to reach a desired status
        @param image_id: The uuid of the image
        @type image_id: String
        @param desired_status: The desired final status of the image
        @type desired_status: String
        @param interval_time: The amount of time in seconds to wait
                              between polling
        @type interval_time: Integer
        @param timeout: The amount of time in seconds to wait
                              before aborting
        @type timeout: Integer
        @return: Response object containing response and the image
                 domain object
        @rtype: requests.Response
        """

        interval_time = interval_time or self.config.image_status_interval
        timeout = timeout or self.config.snapshot_timeout
        end_time = time.time() + timeout

        while time.time() < end_time:
            resp = self.client.get_image(image_id)
            image = resp.entity

            if image.status.lower() == ImageStatus.ERROR.lower():
                raise BuildErrorException(
                    "Build failed. Image with uuid {0} "
                    "entered ERROR status.".format(image.id))

            if image.status == desired_status:
                break
            time.sleep(interval_time)
        else:
            raise TimeoutException(
                "wait_for_image_status ran for {0} seconds and did not "
                "observe image {1} reach the {2} status.".format(
                    timeout, image_id, desired_status))

        return resp

    def create_new_task(self, input_=None, type_=None):
        """@summary: Create new task and wait for success status"""

        if input_ is None:
            input_ = {'image_properties': {},
                      'import_from': self.config.import_from,
                      'import_from_format': self.config.import_from_format}
        if type_ is None:
            type_ = TaskTypes.IMPORT

        failures = []
        attempts = self.config.resource_creation_attempts
        for attempt in range(attempts):
            try:
                response = self.client.create_task(input_=input_, type_=type_)
                task_id = response.entity.id_
                task = self.wait_for_task_status(task_id, TaskStatus.SUCCESS)
                return task
            except (TimeoutException, BuildErrorException) as ex:
                self._log.error('Failed to create task with uuid {0}: '
                                '{1}'.format(task_id, ex.message))
                failures.append(ex.message)
        raise RequiredResourceException(
            'Failed to successfully create a task after {0} attempts: '
            '{1}'.format(attempts, failures))

    def create_new_tasks(self, input_=None, type_=None, count=1):
        """@summary: Create new tasks and wait for success status for each"""

        task_list = []

        for i in range(count):
            task = self.create_new_task(input_=input_, type_=type_)
            task_list.append(task)

        return task_list

    def list_tasks_pagination(self, limit=None, marker=None, sort_dir=None,
                              status=None, type_=None):
        """@summary: Get tasks accounting for pagination as needed"""

        task_list = []
        results_limit = limit or self.config.results_limit

        response = self.client.list_tasks(
            limit=limit, marker=marker, sort_dir=sort_dir, status=status,
            type_=type_)

        tasks = response.entity

        while len(tasks) == results_limit:
            task_list += tasks
            marker = tasks[results_limit - 1].id_
            response = self.client.list_tasks(
                limit=limit, marker=marker, sort_dir=sort_dir, status=status,
                type_=type_)
            tasks = response.entity

        task_list += tasks

        return task_list

    def validate_task(self, task):
        """@summary: Generically validate a task contains crucial expected
        data
        """

        errors = []

        if task.status is None:
            errors.append(self.error_msg.format(
                'status', not None, task.status))
        if self.id_regex.match(task.id_) is None:
            errors.append(self.error_msg.format(
                'id_', not None, self.id_regex.match(task.id_)))
        if task.created_at is None:
            errors.append(self.error_msg.format(
                'created_at', not None, task.created_at))
        if task.type_ == TaskTypes.IMPORT and task.input_.import_from is None:
            errors.append(self.error_msg.format(
                'import_from', not None, task.input_.import_from))
        if (task.type_ == TaskTypes.IMPORT and
                task.input_.import_from_format is None):
            errors.append(self.error_msg.format(
                'import_from_format', not None,
                task.input_.import_from_format))
        if task.type_ == TaskTypes.EXPORT and task.input_.image_uuid is None:
            errors.append(self.error_msg.format(
                'image_uuid', not None, task.input_.image_uuid))
        if (task.type_ == TaskTypes.EXPORT and
                task.input_.receiving_swift_container is None):
            errors.append(self.error_msg.format(
                'receiving_swift_container', not None,
                task.input_.receiving_swift_container))
        if task.updated_at is None:
            errors.append(self.error_msg.format(
                'updated_at', not None, task.updated_at))
        if task.self_ != '/v2/tasks/{0}'.format(task.id_):
            errors.append(self.error_msg.format(
                'self_', '/v2/tasks/{0}'.format(task.id_), task.self_))
        if task.type_ is None:
            errors.append(self.error_msg.format(
                'type_', not None, task.type_))
        if (task.type_ == TaskTypes.IMPORT and task.result is not None and
                self.id_regex.match(task.result.image_id) is None):
            errors.append(self.error_msg.format(
                'image_id', not None,
                self.id_regex.match(task.result.image_id)))
        if (task.type_ == TaskTypes.EXPORT and task.result is not None and
                task.result.export_location is None):
            errors.append(self.error_msg.format(
                'export_location', not None,
                task.result.export_location))
        if task.owner is None:
            errors.append(self.error_msg.format(
                'owner', not None, task.owner))
        if task.message is not None:
            errors.append(self.error_msg.format(
                'message', None, task.message))
        if task.schema != '/v2/schemas/task':
            errors.append(self.error_msg.format(
                'schema', '/v2/schemas/task', task.schema))

        return errors

    def wait_for_task_status(self, task_id, desired_status, client=None,
                             interval_time=None, timeout=None):
        """@summary: Waits for a task to reach a desired status"""

        interval_time = interval_time or self.config.task_status_interval
        timeout = timeout or self.config.task_timeout
        end_time = time.time() + timeout
        client = client if client is not None else self.client

        while time.time() < end_time:
            resp = client.get_task(task_id)
            task = resp.entity

            if ((task.status.lower() == TaskStatus.FAILURE and
                    desired_status != TaskStatus.FAILURE) or
                    (task.status.lower() == TaskStatus.SUCCESS and
                     desired_status != TaskStatus.SUCCESS)):
                raise BuildErrorException(
                    'Task with uuid {0} entered {1} status. Task responded '
                    'with the message {2}'.format(
                        task.id_, task.status, task.message))

            if task.status == desired_status:
                break
            time.sleep(interval_time)
        else:
            raise TimeoutException(
                'Failed to reach the {0} status after {1} seconds for task '
                'with uuid {2}'.format(desired_status, timeout, task_id))

        return task
