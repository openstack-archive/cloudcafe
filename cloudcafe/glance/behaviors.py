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

import calendar
import re
import time

from cafe.engine.behaviors import BaseBehavior
from cloudcafe.common.behaviors import StatusProgressionVerifier
from cloudcafe.common.resources import ResourcePool
from cloudcafe.common.tools.datagen import rand_name
from cloudcafe.compute.common.exceptions import (
    BuildErrorException, RequiredResourceException, TimeoutException)
from cloudcafe.glance.common.constants import ImageProperties, Messages
from cloudcafe.glance.common.types import (
    ImageContainerFormat, ImageDiskFormat, ImageStatus, Schemas, TaskStatus,
    TaskTypes)


class ImagesBehaviors(BaseBehavior):
    """@summary: Behaviors class for Images"""

    def __init__(self, glance_client, glance_config):
        super(ImagesBehaviors, self).__init__()
        self.config = glance_config
        self.client = glance_client
        self.resources = ResourcePool()
        self.error_msg = Messages.ERROR_MSG
        self.id_regex = re.compile(ImageProperties.ID_REGEX)

    @staticmethod
    def read_data_file(file_path):
        """
        @summary: Retrieve data file for a given file path

        @param file_path: Location of data file
        @type file_path: String
        @return: Test_data
        @rtype: String
        """
        try:
            with open(file_path, "r") as DATA:
                test_data = DATA.read().rstrip()
        except IOError as file_error:
            raise file_error

        return test_data

    def create_image_via_task(self, image_properties=None, import_from=None):
        """
        @summary: Create new image via task

        @param image_properties: Properties to use for the image creation
        @type image_properties: Dictionary
        @param import_from: Location of image
        @type import_from: String
        @return: Image
        @rtype: Object
        """

        image_properties = image_properties or {'name': rand_name('image')}
        import_from = import_from or self.config.import_from

        input_ = {'image_properties': image_properties,
                  'import_from': import_from}
        task = self.create_new_task(input_=input_, type_=TaskTypes.IMPORT)
        image_id = task.result.image_id

        self.client.add_image_tag(image_id=image_id, tag=rand_name('tag'))

        response = self.client.get_image_details(image_id=image_id)
        image = response.entity

        return image

    def create_images_via_task(self, image_properties=None, import_from=None,
                               count=2):
        """
        @summary: Create new images via tasks

        @param image_properties: Properties to use for the image creation
        @type image_properties: Dictionary
        @param import_from: Location of image
        @type import_from: String
        @param count: Number of images to create
        @type count: Integer
        @return: Image_list
        @rtype: List
        """

        image_list = []

        for i in range(count):
            image = self.create_image_via_task(
                image_properties=image_properties, import_from=import_from)
            image_list.append(image)

        return image_list

    def register_new_image(self, container_format=None, disk_format=None,
                           name=None, protected=None, tags=None):
        """
        @summary: Register new image and add it for deletion

        @param container_format: Format of source container
        @type container_format: String
        @param disk_format: Format of source disk
        @type disk_format: String
        @param name: Name of image
        @type name: String
        @param protected: Flag to determine if image is able to be deleted
        @type protected: Boolean
        @param tags: Tags to be added to the image
        @type tags: Dictionary
        @return: Image
        @rtype: Object
        """

        container_format = container_format or ImageContainerFormat.BARE
        disk_format = disk_format or ImageDiskFormat.RAW
        name = name or rand_name('image')

        response = self.client.register_image(
            container_format=container_format, disk_format=disk_format,
            name=name, protected=protected, tags=tags)
        image = response.entity

        if image is not None:
            self.resources.add(image.id_, self.client.delete_image)

        return image

    def register_new_images(self, container_format=None, disk_format=None,
                            name=None, protected=None, tags=None, count=2):
        """
        @summary: Register new images and add them for deletion

        @param container_format: Format of source container
        @type container_format: String
        @param disk_format: Format of source disk
        @type disk_format: String
        @param name: Name of image
        @type name: String
        @param protected: Flag to determine if image is able to be deleted
        @type protected: Boolean
        @param tags: Tags to be added to the image
        @type tags: Dictionary
        @param count: Number of images to register
        @type count: Integer
        @return: Image_list
        @rtype: List
        """

        image_list = []

        for i in range(count):
            image = self.register_new_image(
                container_format=container_format, disk_format=disk_format,
                name=name, protected=protected, tags=tags)
            image_list.append(image)

        return image_list

    def list_all_images(self, **params):
        """
        @summary: Retrieve a complete list of images accounting for any
        query parameters

        @param params: Parameters to alter the returned list of images
        @type params: Dictionary
        @return: Image_list
        @rtype: List
        """

        image_list = []
        results_limit = self.config.results_limit

        response = self.client.list_images(params)
        images = response.entity

        while len(images) == results_limit:
            image_list += images
            marker = images[results_limit - 1].id_
            params.update({"marker": marker})
            response = self.client.list_images(params)
            images = response.entity

        image_list += images

        return image_list

    def list_all_image_member_ids(self, image_id):
        """
        @summary: Retrieve a complete list of image member ids

        @param image_id: Image id to retrieve image members for
        @type image_id: UUID
        @return: members
        @rtype: List
        """

        response = self.client.list_members(image_id)
        members = response.entity

        return [member.member_id for member in members]

    @staticmethod
    def get_time_delta(time_in_sec, time_property):
        """
        @summary: Calculate the difference between an image attribute's time
        value and a time_property

        @param time_in_sec: Current time in seconds
        @type time_in_sec: Integer
        @param time_property: Image property containing a time
        @type time_property: Datetime
        @return: Time_delta
        @rtype: Integer
        """

        time_property_in_sec = calendar.timegm(time_property.timetuple())

        return abs(time_property_in_sec - time_in_sec)

    def validate_image(self, image):
        """
        @summary: Generically validate an image contains crucial expected
        data

        @param image: Image to be validated
        @type image: Object
        @return: Errors
        @rtype: List
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
        """
        @summary: Generically validate an image member contains crucial
        expected data

        @param image_id: Image containing image members
        @type image_id: UUID
        @param image_member: Image member to be validated
        @type image_member: Object
        @param member_id: Image member id to compare against
        @type member_id: Integer
        @return: Errors
        @rtype: List
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
                              interval_time=15, timeout=900):
        """
        @summary: Wait for a image to reach a desired status

        @param image_id: Image id to evaluate
        @type image_id: UUID
        @param desired_status: Expected final status of image
        @type desired_status: String
        @param interval_time: Amount of time in seconds to wait between polling
        @type interval_time: Integer
        @param timeout: Amount of time in seconds to wait before aborting
        @type timeout: Integer
        @return: Resp
        @rtype: Object
        """

        interval_time = interval_time or self.config.image_status_interval
        timeout = timeout or self.config.snapshot_timeout
        end_time = time.time() + timeout

        while time.time() < end_time:
            resp = self.client.get_image_details(image_id)
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
        """
        @summary: Create new task and wait for success status

        @param input_: Image properties and location data
        @type input_: Dictionary
        @param type_: Type of task
        @type type_: String
        @return: Task
        @rtype: Object
        """

        import_from = self.config.import_from
        input_ = input_ or {'image_properties': {},
                            'import_from': import_from}
        type_ = type_ or TaskTypes.IMPORT
        failures = []
        attempts = self.config.resource_creation_attempts

        for attempt in range(attempts):
            try:
                resp = self.client.task_to_import_image(input_=input_,
                                                        type_=type_)
                task_id = resp.entity.id_
                task = self.wait_for_task_status(task_id, TaskStatus.SUCCESS)
                return task
            except (BuildErrorException, TimeoutException) as ex:
                failure = ('Attempt {0}: Failed to create task with '
                           'the message '
                           '{1}'.format(attempt + 1, ex.message))
                self._log.error(failure)
                failures.append(failure)
        raise RequiredResourceException(
            'Failed to successfully create a task after {0} attempts: '
            '{1}'.format(attempts, failures))

    def create_new_tasks(self, input_=None, type_=None, count=2):
        """
        @summary: Create new tasks and wait for success status for each

        @param input_: Image properties and image location
        @type input_: Dictionary
        @param type_: Type of task
        @type type_: String
        @param count: Number of tasks to create
        @type count: Integer
        @return: Task_list
        @rtype: List
        """

        task_list = []

        for i in range(count):
            task = self.create_new_task(input_=input_, type_=type_)
            task_list.append(task)

        return task_list

    def list_all_tasks(self, limit=None, marker=None, sort_dir=None,
                       status=None, type_=None):
        """
        @summary: Retrieve a complete list of tasks accounting for query
        parameters

        @param limit: Number of tasks to return
        @type limit: Integer
        @param marker: Task to start from
        @type marker: UUID
        @param sort_dir: Direction in which tasks will be returned
        @type sort_dir: String
        @param status: Status of tasks to return
        @type status: String
        @param type_: Type of tasks to return
        @type type_: String
        @return: Task_list
        @rtype: List
        """

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
        """
        @summary: Generically validate a task contains crucial expected
        data

        @param task: Task to be validated
        @type task: UUID
        @return: Errors
        @rtype: List
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
        if task.message != '':
            errors.append(self.error_msg.format(
                'message', '', task.message))
        if task.schema != '/v2/schemas/task':
            errors.append(self.error_msg.format(
                'schema', '/v2/schemas/task', task.schema))

        return errors

    def validate_exported_files(self, expect_success, files, image_id):
        """
        @summary: Validate that a given storage location contains a
        given file or not

        @param expect_success: Flag to determine if tasks completed
        successfully
        @type expect_success: Boolean
        @param files: File objects to be validated
        @type files: List
        @param image_id: Image id to validate against
        @type image_id: UUID
        @return: Errors, file_names
        @rtype: List, list
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

    def wait_for_task_status(self, task_id, desired_status, interval_time=10,
                             timeout=1200):
        """
        @summary: Waits for a task to reach a desired status

        @param task_id: Task id to evaluate
        @type task_id: UUID
        @param desired_status: Expected final status of task
        @type desired_status: String
        @param interval_time: Amount of time in seconds to wait between polling
        @type interval_time: Integer
        @param timeout: Amount of time in seconds to wait before aborting
        @type timeout: Integer
        @return: Task
        @rtype: Object
        """

        interval_time = interval_time or self.config.task_status_interval
        timeout = timeout or self.config.task_timeout
        end_time = time.time() + timeout

        while time.time() < end_time:
            resp = self.client.get_task_details(task_id)
            task = resp.entity

            if ((task.status.lower() == TaskStatus.FAILURE and
                    desired_status != TaskStatus.FAILURE) or
                    (task.status.lower() == TaskStatus.SUCCESS and
                     desired_status != TaskStatus.SUCCESS)):
                raise BuildErrorException(
                    'Task with uuid {0} entered {1} status. Task responded '
                    'with the message {2}'.format(
                        task.id_, task.status, task.message.replace('\\', '')))

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

    def create_task_with_transitions(self, input_, task_type, outcome,
                                     final_status=None):
        """
        @summary: Create a task and verify that it transitions through the
        expected statuses

        @param input_: Image properties and location data
        @type input_: Dictionary
        @param task_type: Type of task
        @type task_type: String
        @param outcome: Expected final status
        @type outcome: Integer
        @param final_status: Flag to determine success or failure
        @type final_status: String
        @return: Task
        @rtype: Object
        """

        response = self.client.create_task(
            input_=input_, type_=task_type)
        task = response.entity

        response = self.client.get_task_details(task.id_)
        task_status = response.entity.status.lower()

        # Verify task progresses as expected
        verifier = StatusProgressionVerifier(
            'task', task.id_, task_status, task.id_)

        verifier.add_state(
            expected_statuses=[TaskStatus.PENDING],
            acceptable_statuses=[TaskStatus.PROCESSING, outcome],
            error_statuses=[TaskStatus.SUCCESS],
            timeout=self.config.task_timeout, poll_rate=1)

        verifier.add_state(
            expected_statuses=[TaskStatus.PROCESSING],
            acceptable_statuses=[outcome],
            error_statuses=[TaskStatus.PENDING, TaskStatus.SUCCESS],
            timeout=self.config.task_timeout, poll_rate=1)

        if final_status == TaskStatus.SUCCESS:
            verifier.add_state(
                expected_statuses=[TaskStatus.SUCCESS],
                error_statuses=[TaskStatus.PENDING, TaskStatus.FAILURE],
                timeout=self.config.task_timeout, poll_rate=1)

        if final_status == TaskStatus.FAILURE:
            verifier.add_state(
                expected_statuses=[TaskStatus.FAILURE],
                error_statuses=[TaskStatus.PENDING, TaskStatus.SUCCESS],
                timeout=self.config.task_timeout, poll_rate=1)

        verifier.start()

        response = self.client.get_task_details(task.id_)
        return response.entity
