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
from cloudcafe.common.behaviors import StatusProgressionVerifier
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

    def create_image_via_task(self, image_properties=None, import_from=None,
                              import_from_format=None):
        """
        @summary: Create new image via the create new task method and add it
        for deletion
        """

        image_properties = image_properties or {'name': rand_name('image')}
        import_from = import_from or self.config.import_from
        import_from_format = import_from or self.config.import_from_format

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

    def create_images_via_task(self, image_properties=None, import_from=None,
                               import_from_format=None, count=1):
        """
        @summary: Create new images via the create new task method and add them
        for deletion
        """

        image_list = []

        for i in range(count):
            image = self.create_image_via_task(
                image_properties=image_properties, import_from=import_from,
                import_from_format=import_from_format)
            image_list.append(image)

        return image_list

    def create_new_image(self, container_format=None, disk_format=None,
                         name=None, protected=None, tags=None):
        """@summary: Create new image and add it for deletion"""

        container_format = container_format or ImageContainerFormat.BARE
        disk_format = disk_format or ImageDiskFormat.RAW
        name = name or rand_name('image')

        response = self.client.create_image(
            container_format=container_format, disk_format=disk_format,
            name=name, protected=protected, tags=tags)
        image = response.entity

        if image is not None:
            self.resources.add(image.id_, self.client.delete_image)

        return image

    def create_new_images(self, container_format=None, disk_format=None,
                          name=None, protected=None, tags=None, count=1):
        """@summary: Create new images and add them for deletion"""

        image_list = []

        for i in range(count):
            image = self.create_new_image(
                container_format=container_format, disk_format=disk_format,
                name=name, protected=protected, tags=tags)
            image_list.append(image)

        return image_list

    def list_images_pagination(self, **filters):
        """
        @summary: Get images accounting for pagination as needed with
        variable number of filter arguments
        """

        image_list = []
        results_limit = self.config.results_limit

        response = self.client.list_images(filters=filters)
        images = response.entity

        while len(images) == results_limit:
            image_list += images
            marker = images[results_limit - 1].id_
            filters.update({"marker": marker})
            response = self.client.list_images(filters=filters)
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

        if image.auto_disk_config is None:
            errors.append(self.error_msg.format(
                'auto_disk_config', 'not None', image.auto_disk_config))
        if image.created_at is None:
            errors.append(self.error_msg.format(
                'created_at', 'not None', image.created_at))
        if image.file_ != '/v2/images/{0}/file'.format(image.id_):
            errors.append(self.error_msg.format(
                'file_', '/v2/images/{0}/file'.format(image.id_), image.file_))
        if image.image_type is None:
            errors.append(self.error_msg.format(
                'image_type', 'not None', image.image_type))
        if self.id_regex.match(image.id_) is None:
            errors.append(self.error_msg.format(
                'id_', 'not None', self.id_regex))
        if image.min_disk is None:
            errors.append(self.error_msg.format(
                'min_disk', 'not None', image.min_disk))
        if image.min_ram is None:
            errors.append(self.error_msg.format(
                'min_ram', 'not None', image.min_ram))
        if image.os_type is None:
            errors.append(self.error_msg.format(
                'os_type', 'not None', image.os_type))
        if image.protected is None:
            errors.append(self.error_msg.format(
                'protected', 'not None', image.protected))
        if image.schema != Schemas.IMAGE_SCHEMA:
            errors.append(self.error_msg.format(
                'schema', Schemas.IMAGE_SCHEMA, image.schema))
        if image.self_ != '/v2/images/{0}'.format(image.id_):
            errors.append(self.error_msg.format(
                'schema', '/v2/images/{0}'.format(image.id_), image.self_))
        if image.status is None:
            errors.append(self.error_msg.format(
                'status', 'not None', image.status))
        if image.updated_at is None:
            errors.append(self.error_msg.format(
                'updated_at', 'not None', image.updated_at))
        if image.user_id is None:
            errors.append(self.error_msg.format(
                'user_id', 'not None', image.user_id))

        return errors

    def validate_image_member(self, image_id, image_member, member_id):
        """@summary: Generically validate an image member contains crucial
        expected data
        """

        errors = []

        if image_member.created_at is None:
            errors.append(self.error_msg.format(
                'created_at', 'not None', image_member.created_at))
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
            errors.append(self.error_msg.format(
                'status', 'not None', image_member.status))
        if image_member.updated_at is None:
            errors.append(self.error_msg.format(
                'updated_at', 'not None', image_member.updated_at))

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

        import_from = self.config.import_from
        import_from_format = self.config.import_from_format
        input_ = input_ or {'image_properties': {},
                            'import_from': import_from,
                            'import_from_format': import_from_format}
        type_ = type_ or TaskTypes.IMPORT
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
                'status', 'not None', task.status))
        if self.id_regex.match(task.id_) is None:
            errors.append(self.error_msg.format(
                'id_', 'not None', self.id_regex.match(task.id_)))
        if task.created_at is None:
            errors.append(self.error_msg.format(
                'created_at', 'not None', task.created_at))
        if task.type_ == TaskTypes.IMPORT:
            if task.input_.import_from is None:
                errors.append(self.error_msg.format(
                    'import_from', 'not None', task.input_.import_from))
            if (task.result is not None and
                    self.id_regex.match(task.result.image_id) is None):
                errors.append(self.error_msg.format(
                    'image_id', 'not None',
                    self.id_regex.match(task.result.image_id)))
        elif task.type_ == TaskTypes.EXPORT:
            if task.input_.image_uuid is None:
                errors.append(self.error_msg.format(
                    'image_uuid', 'not None', task.input_.image_uuid))
            if task.input_.receiving_swift_container is None:
                errors.append(self.error_msg.format(
                    'receiving_swift_container', 'not None',
                    task.input_.receiving_swift_container))
            if task.result is not None and task.result.export_location is None:
                errors.append(self.error_msg.format(
                    'export_location', 'not None',
                    task.result.export_location))
        elif task.type_ is None:
            errors.append(self.error_msg.format(
                'type_', 'not None', task.type_))
        if task.updated_at is None:
            errors.append(self.error_msg.format(
                'updated_at', 'not None', task.updated_at))
        if task.self_ != '/v2/tasks/{0}'.format(task.id_):
            errors.append(self.error_msg.format(
                'self_', '/v2/tasks/{0}'.format(task.id_), task.self_))
        if task.owner is None:
            errors.append(self.error_msg.format(
                'owner', 'not None', task.owner))
        if task.message != 'None':
            errors.append(self.error_msg.format(
                'message', 'None', task.message))
        if task.schema != '/v2/schemas/task':
            errors.append(self.error_msg.format(
                'schema', '/v2/schemas/task', task.schema))

        return errors

    def validate_exported_files(self, export_to, expect_success, files,
                                image_id):
        """
        @summary: Validate that a given cloud files location contains a
        given file or not
        """

        errors = []
        file_names = [file_.name for file_ in files]

        if expect_success:
            if '{0}.vhd'.format(image_id) not in file_names:
                errors.append(self.error_msg.format(
                    'file present', True, False))
        else:
            if '{0}.vhd'.format(image_id) in file_names:
                errors.append(self.error_msg.format(
                    'file present', False, True))

        return errors, file_names

    def wait_for_task_status(self, task_id, desired_status, interval_time=None,
                             timeout=None):
        """@summary: Waits for a task to reach a desired status"""

        interval_time = interval_time or self.config.task_status_interval
        timeout = timeout or self.config.task_timeout
        end_time = time.time() + timeout

        while time.time() < end_time:
            resp = self.client.get_task(task_id)
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

        if (task is not None and task.type_ == TaskTypes.IMPORT and
                task.status.lower() == TaskStatus.SUCCESS):
            self.resources.add(task.result.image_id, self.client.delete_image)

        return task

    def get_task_status(self, task_id):
        """@summary: Retrieve task status"""

        response = self.client.get_task(task_id)
        return response.entity.status.lower()

    def create_task_with_transitions(self, input_, task_type,
                                     final_status=None):
        """
        @summary: Create a task and verify that it transitions through the
        expected statuses
        """

        response = self.client.create_task(
            input_=input_, type_=task_type)
        task = response.entity

        # Verify task progresses as expected
        verifier = StatusProgressionVerifier(
            'task', task.id_, self.get_task_status, task.id_)

        verifier.add_state(
            expected_statuses=[TaskStatus.PENDING],
            acceptable_statuses=[TaskStatus.PROCESSING, TaskStatus.SUCCESS],
            error_statuses=[TaskStatus.FAILURE],
            timeout=self.config.task_timeout, poll_rate=1)

        verifier.add_state(
            expected_statuses=[TaskStatus.PROCESSING],
            acceptable_statuses=[TaskStatus.SUCCESS],
            error_statuses=[TaskStatus.FAILURE],
            timeout=self.config.task_timeout, poll_rate=1)

        if final_status == TaskStatus.SUCCESS:
            verifier.add_state(
                expected_statuses=[TaskStatus.SUCCESS],
                error_statuses=[TaskStatus.FAILURE],
                timeout=self.config.task_timeout, poll_rate=1)

        verifier.start()

        response = self.client.get_task(task.id_)
        return response.entity
