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
    """@summary: Behaviors for Images"""

    def __init__(self, images_client, images_config):
        super(ImagesBehaviors, self).__init__()
        self.config = images_config
        self.client = images_client
        self.resources = ResourcePool()

    @staticmethod
    def get_comparison_data(data_file):
        """
        @summary: Create comparison dictionary based on a given set of data

        @param data_file: File containing data to compare
        @param data_file: String

        @return: Comparison_dict
        @rtype: Dictionary
        """

        comparison_dict = dict()
        data_columns = []

        with open(data_file, 'r') as DATA:
                all_data = DATA.readlines()

        for line in all_data:
            # Skip any comments or short lines
            if line.startswith('#') or len(line) < 5:
                continue

            # Get the defined data
            if line.startswith('+'):
                line = line.replace('+', '')
                data_columns = [x.strip().lower() for x in line.split('|')]
                continue

            # Process the data
            each_data = dict()
            data = [x.strip() for x in line.split('|')]
            for x, y in zip(data_columns[1:], data[1:]):
                each_data[x] = y

            comparison_dict[data[0]] = each_data

        return comparison_dict

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

        resp = self.client.get_image_details(image_id=image_id)
        image = self.verify_resp(resp, 'get image details', image_id)

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

    def register_new_image(self, auto_disk_config=None, checksum=None,
                           container_format=None, created_at=None,
                           disk_format=None, file_=None, id_=None,
                           image_type=None, min_disk=None, min_ram=None,
                           name=None, os_type=None, owner=None, protected=None,
                           schema=None, self_=None, size=None, status=None,
                           tags=None, updated_at=None, user_id=None,
                           visibility=None, additional_properties=None):
        """
        @summary: Register new image and add it for deletion

        @param auto_disk_config: Auto disk config for the image being created
        @type auto_disk_config: String
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
        @param image_type: Image type for the image being created
        @type image_type: String
        @param min_disk: Minimum disk for the image being created
        @type min_disk: String
        @param min_ram: Minimum ram for the image being created
        @type min_ram: String
        @param name: Name for the image being created
        @type name: String
        @param os_type: OS type for the image being created
        @type os_type: String
        @param owner: Owner for the image being created
        @type owner: String
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
        @param user_id: User id for the image being created
        @type user_id: String
        @param visibility: Visibility for the image being created
        @type visibility: String
        @param additional_properties: Additional properties for the image being
        created
        @type additional_properties: Dictionary

        @return: Image
        @rtype: Object
        """

        container_format = container_format or ImageContainerFormat.BARE
        disk_format = disk_format or ImageDiskFormat.RAW
        name = name or rand_name('image')

        resp = self.client.register_image(
            auto_disk_config=auto_disk_config, checksum=checksum,
            container_format=container_format, created_at=created_at,
            disk_format=disk_format, file_=file_, id_=id_,
            image_type=image_type,  min_disk=min_disk, min_ram=min_ram,
            name=name, os_type=os_type, owner=owner, protected=protected,
            schema=schema, self_=self_, size=size, status=status,
            tags=tags, updated_at=updated_at, user_id=user_id,
            visibility=visibility, additional_properties=additional_properties)
        image = self.verify_resp(resp, 'register image')

        self.resources.add(image.id_, self.client.delete_image)

        return image

    def register_new_images(self, auto_disk_config=None, checksum=None,
                            container_format=None, created_at=None,
                            disk_format=None, file_=None, id_=None,
                            image_type=None, min_disk=None, min_ram=None,
                            name=None, os_type=None, owner=None,
                            protected=None, schema=None, self_=None, size=None,
                            status=None, tags=None, updated_at=None,
                            user_id=None, visibility=None,
                            additional_properties=None, count=2):
        """
        @summary: Register new images and add them for deletion

        @param auto_disk_config: Auto disk config for the image being created
        @type auto_disk_config: String
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
        @param image_type: Image type for the image being created
        @type image_type: String
        @param min_disk: Minimum disk for the image being created
        @type min_disk: String
        @param min_ram: Minimum ram for the image being created
        @type min_ram: String
        @param name: Name for the image being created
        @type name: String
        @param os_type: OS type for the image being created
        @type os_type: String
        @param owner: Owner for the image being created
        @type owner: String
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
        @param user_id: User id for the image being created
        @type user_id: String
        @param visibility: Visibility for the image being created
        @type visibility: String
        @param additional_properties: Additional properties for the image being
        created
        @type additional_properties: Dictionary

        @return: Image_list
        @rtype: List
        """

        image_list = []

        for i in range(count):
            image = self.register_new_image(
                auto_disk_config=auto_disk_config, checksum=checksum,
                container_format=container_format, created_at=created_at,
                disk_format=disk_format, file_=file_, id_=id_,
                image_type=image_type,  min_disk=min_disk, min_ram=min_ram,
                name=name, os_type=os_type, owner=owner, protected=protected,
                schema=schema, self_=self_, size=size, status=status,
                tags=tags, updated_at=updated_at, user_id=user_id,
                visibility=visibility,
                additional_properties=additional_properties)
            image_list.append(image)

        return image_list

    def list_all_images(self, url_addition=None, **params):
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
        params.update({'limit': results_limit})

        resp = self.client.list_images(params, url_addition)
        images = self.verify_resp(resp, 'list images')

        while len(images) == results_limit:
            image_list += images

            marker = images[results_limit - 1].id_
            params.update({'marker': marker})

            resp = self.client.list_images(params, url_addition)
            images = self.verify_resp(resp, 'list images')

        image_list += images

        return image_list

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

    @staticmethod
    def validate_image(image):
        """
        @summary: Generically validate an image contains crucial expected
        data

        @param image: Image to be validated
        @type image: Object

        @return: Errors
        @rtype: List
        """

        id_regex = re.compile(ImageProperties.ID_REGEX)
        errors = []

        # The following properties do not always have values:
        # checksum, container_format, disk_format, name, tags

        if image.auto_disk_config is None:
            errors.append(Messages.PROPERTY_MSG.format(
                'auto_disk_config', 'not None', image.auto_disk_config))
        if image.created_at is None:
            errors.append(Messages.PROPERTY_MSG.format(
                'created_at', 'not None', image.created_at))
        if image.file_ != '/v2/images/{0}/file'.format(image.id_):
            errors.append(Messages.PROPERTY_MSG.format(
                'file', '/v2/images/{0}/file'.format(image.id_), image.file_))
        if id_regex.match(image.id_) is None:
            errors.append(Messages.PROPERTY_MSG.format(
                'id', 'not None', id_regex))
        if image.image_type is None:
            errors.append(Messages.PROPERTY_MSG.format(
                'image_type', 'not None', image.image_type))
        if image.min_disk is None:
            errors.append(Messages.PROPERTY_MSG.format(
                'min_disk', 'not None', image.min_disk))
        if image.min_ram is None:
            errors.append(Messages.PROPERTY_MSG.format(
                'min_ram', 'not None', image.min_ram))
        if image.os_type is None:
            errors.append(Messages.PROPERTY_MSG.format(
                'os_type', 'not None', image.os_type))
        if image.owner is None:
            errors.append(Messages.PROPERTY_MSG.format(
                'owner', 'not None', image.owner))
        if image.protected is None:
            errors.append(Messages.PROPERTY_MSG.format(
                'protected', 'not None', image.protected))
        if image.schema != Schemas.IMAGE_SCHEMA:
            errors.append(Messages.PROPERTY_MSG.format(
                'schema', Schemas.IMAGE_SCHEMA, image.schema))
        if image.self_ != '/v2/images/{0}'.format(image.id_):
            errors.append(Messages.PROPERTY_MSG.format(
                'self', '/v2/images/{0}'.format(image.id_), image.self_))
        if image.status is None:
            errors.append(Messages.PROPERTY_MSG.format(
                'status', 'not None', image.status))
        if image.updated_at is None:
            errors.append(Messages.PROPERTY_MSG.format(
                'updated_at', 'not None', image.updated_at))
        if image.user_id is None:
            errors.append(Messages.PROPERTY_MSG.format(
                'user_id', 'not None', image.user_id))
        if image.virtual_size is not None:
            errors.append(Messages.PROPERTY_MSG.format(
                'virtual_size', 'None', image.virtual_size))
        if image.visibility is None:
            errors.append(Messages.PROPERTY_MSG.format(
                'visibility', 'not None', image.visibility))

        return errors

    @staticmethod
    def validate_image_member(image_member):
        """
        @summary: Generically validate an image member contains crucial
        expected data

        @param image_member: Image member to be validated
        @type image_member: Object

        @return: Errors
        @rtype: List
        """

        errors = []

        if image_member.created_at is None:
            errors.append(Messages.PROPERTY_MSG.format(
                'created_at', 'not None', image_member.created_at))
        if image_member.image_id is None:
            errors.append(Messages.PROPERTY_MSG.format(
                'image_id', 'not None', image_member.image_id))
        if image_member.member_id is None:
            errors.append(Messages.PROPERTY_MSG.format(
                'member_id', 'not None', image_member.member_id))
        if image_member.schema != Schemas.IMAGE_MEMBER_SCHEMA:
            errors.append(Messages.PROPERTY_MSG.format(
                'schema', Schemas.IMAGE_MEMBER_SCHEMA, image_member.schema))
        if image_member.status is None:
            errors.append(Messages.PROPERTY_MSG.format(
                'status', 'not None', image_member.status))
        if image_member.updated_at is None:
            errors.append(Messages.PROPERTY_MSG.format(
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
            image = self.verify_resp(resp, 'get image details', image_id)

            if image.status.lower() == ImageStatus.ERROR.lower():
                raise BuildErrorException(
                    'Image with the uuid {0} entered ERROR '
                    'status.'.format(image_id))

            if image.status == desired_status:
                break

            time.sleep(interval_time)
        else:
            raise TimeoutException(
                'Image with the uuid {0} did not reach the {1} status within '
                '{2} seconds.'.format(image_id, desired_status, timeout))

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
                if type_ == TaskTypes.IMPORT:
                    resp = self.client.task_to_import_image(input_=input_,
                                                            type_=type_)
                else:
                    resp = self.client.task_to_export_image(input_=input_,
                                                            type_=type_)
                task = resp.entity

                task = self.wait_for_task_status(task.id_, TaskStatus.SUCCESS)

                return task

            except (BuildErrorException, TimeoutException) as ex:
                failure = ('Attempt {0}: Failed to create task with '
                           'the message {1}'.format(attempt + 1, ex.message))
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

    def list_all_tasks(self, **params):
        """
        @summary: Retrieve a complete list of tasks accounting for query
        parameters

        @param params: Parameters to alter the returned list of images
        @type params: Dictionary

        @return: Task_list
        @rtype: List
        """

        task_list = []
        results_limit = self.config.results_limit
        params.update({'limit': results_limit})

        resp = self.client.list_tasks(params)
        tasks = self.verify_resp(resp, 'list tasks')

        while len(tasks) == results_limit:
            task_list += tasks

            marker = tasks[results_limit - 1].id_
            params.update({'marker': marker})

            resp = self.client.list_tasks(params)
            tasks = self.verify_resp(resp, 'list tasks')

        task_list += tasks

        return task_list

    @staticmethod
    def validate_task(task):
        """
        @summary: Generically validate a task contains crucial expected
        data

        @param task: Task to be validated
        @type task: UUID

        @return: Errors
        @rtype: List
        """

        id_regex = re.compile(ImageProperties.ID_REGEX)
        errors = []

        if task.status is None:
            errors.append(Messages.PROPERTY_MSG.format(
                'status', 'not None', task.status))
        if id_regex.match(task.id_) is None:
            errors.append(Messages.PROPERTY_MSG.format(
                'id_', 'not None', id_regex.match(task.id_)))
        if task.created_at is None:
            errors.append(Messages.PROPERTY_MSG.format(
                'created_at', 'not None', task.created_at))
        if task.type_ == TaskTypes.IMPORT:
            if task.input_.import_from is None:
                errors.append(Messages.PROPERTY_MSG.format(
                    'import_from', 'not None', task.input_.import_from))
            if (task.result is not None and
                    id_regex.match(task.result.image_id) is None):
                errors.append(Messages.PROPERTY_MSG.format(
                    'image_id', 'not None',
                    id_regex.match(task.result.image_id)))
        elif task.type_ == TaskTypes.EXPORT:
            if task.input_.image_uuid is None:
                errors.append(Messages.PROPERTY_MSG.format(
                    'image_uuid', 'not None', task.input_.image_uuid))
            if task.input_.receiving_swift_container is None:
                errors.append(Messages.PROPERTY_MSG.format(
                    'receiving_swift_container', 'not None',
                    task.input_.receiving_swift_container))
            if task.result is not None and task.result.export_location is None:
                errors.append(Messages.PROPERTY_MSG.format(
                    'export_location', 'not None',
                    task.result.export_location))
        elif task.type_ is None:
            errors.append(Messages.PROPERTY_MSG.format(
                'type_', 'not None', task.type_))
        if task.updated_at is None:
            errors.append(Messages.PROPERTY_MSG.format(
                'updated_at', 'not None', task.updated_at))
        if task.self_ != '/v2/tasks/{0}'.format(task.id_):
            errors.append(Messages.PROPERTY_MSG.format(
                'self_', '/v2/tasks/{0}'.format(task.id_), task.self_))
        if task.owner is None:
            errors.append(Messages.PROPERTY_MSG.format(
                'owner', 'not None', task.owner))
        if task.message != '':
            errors.append(Messages.PROPERTY_MSG.format(
                'message', 'Empty message', task.message))
        if task.schema != '/v2/schemas/task':
            errors.append(Messages.PROPERTY_MSG.format(
                'schema', '/v2/schemas/task', task.schema))

        return errors

    @staticmethod
    def validate_exported_files(expect_success, files, image_id):
        """
        @summary: Validate that a given storage location contains a
        given file or not

        @param expect_success: Flag to determine if task completed successfully
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
                errors.append('Expected VHD file not listed. Expected: '
                              '{0}.vhd to be listed Received: File was not '
                              'listed'.format(image_id))
        else:
            if '{0}.vhd'.format(image_id) in file_names:
                errors.append('Unexpected VHD file listed. Expected: {0}.vhd '
                              'to not be listed Received: File was '
                              'listed'.format(image_id))

        return errors, file_names

    def wait_for_task_status(self, task_id, desired_status, interval_time=10,
                             timeout=1200):
        """
        @summary: Waits for a task to reach a desired status and if the import
        task is successful, adds the created image to the resource pool for
        tear down

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
            task = self.verify_resp(resp, 'get task details', task_id)

            if ((task.status.lower() == TaskStatus.FAILURE and
                    desired_status != TaskStatus.FAILURE) or
                    (task.status.lower() == TaskStatus.SUCCESS and
                     desired_status != TaskStatus.SUCCESS)):
                raise BuildErrorException(
                    'Task with the uuid {0} entered the {1} status. Task '
                    'responded with the message {2}'.format(
                        task.id_, task.status, task.message.replace('\\', '')))

            if task.status == desired_status:
                break
            time.sleep(interval_time)
        else:
            raise TimeoutException(
                'Task with the uuid {0} did not reach the {1} status within '
                '{2} seconds.'.format(task_id, desired_status, timeout))

        if (task is not None and task.type_ == TaskTypes.IMPORT and
                task.status.lower() == TaskStatus.SUCCESS):
            self.resources.add(task.result.image_id,
                               self.client.delete_image)

        return task

    def create_task_with_transitions(self, input_, task_type,
                                     final_status=None):
        """
        @summary: Create a task and verify that it transitions through the
        expected statuses

        @param input_: Image properties and location data
        @type input_: Dictionary
        @param task_type: Type of task
        @type task_type: String
        @param final_status: Flag to determine success or failure
        @type final_status: String

        @return: Task
        @rtype: Object
        """

        if task_type == TaskTypes.IMPORT:
            resp = self.client.task_to_import_image(input_, TaskTypes.IMPORT)
        else:
            resp = self.client.task_to_export_image(input_, TaskTypes.EXPORT)

        task = self.verify_resp(resp, 'create task')

        # Verify task progresses as expected
        verifier = StatusProgressionVerifier(
            'task', task.id_, self.get_task_status, task.id_)

        if final_status == TaskStatus.SUCCESS:
            error_statuses = [TaskStatus.FAILURE]
        else:
            error_statuses = [TaskStatus.SUCCESS]

        verifier.add_state(
            expected_statuses=[TaskStatus.PENDING],
            acceptable_statuses=[TaskStatus.PROCESSING, final_status],
            error_statuses=error_statuses,
            timeout=self.config.task_timeout, poll_rate=1)

        if final_status == TaskStatus.SUCCESS:
            error_statuses = [TaskStatus.PENDING, TaskStatus.FAILURE]
        else:
            error_statuses = [TaskStatus.PENDING, TaskStatus.SUCCESS]

        verifier.add_state(
            expected_statuses=[TaskStatus.PROCESSING],
            acceptable_statuses=[final_status],
            error_statuses=error_statuses,
            timeout=self.config.task_timeout, poll_rate=1)

        if final_status == TaskStatus.SUCCESS:
            verifier.add_state(
                expected_statuses=[TaskStatus.SUCCESS],
                error_statuses=[TaskStatus.PENDING, TaskStatus.FAILURE],
                timeout=self.config.task_timeout, poll_rate=1)
        else:
            verifier.add_state(
                expected_statuses=[TaskStatus.FAILURE],
                error_statuses=[TaskStatus.PENDING, TaskStatus.SUCCESS],
                timeout=self.config.task_timeout, poll_rate=1)

        verifier.start()

        return self.client.get_task_details(task.id_).entity

    def get_task_status(self, task_id):
        """
        @summary: Retrieve task status for the status progression verifier in
        the create_task_with_transitions method

        @param task_id: Task id
        @type task_id: UUID

        @return: Status
        @rtype: String
        """

        resp = self.client.get_task_details(task_id)
        task = self.verify_resp(resp, 'get task details', task_id)

        return task.status.lower()

    @staticmethod
    def verify_resp(resp, req, obj_id=None):
        """
        @summary: Verify that a request was successful and that an entity was
        properly deserialized

        @param resp: Response object to verify
        @type resp: Object

        @return: Resp.entity
        @rtype: Object
        """

        if not resp.ok:
            msg = ('Request for {0} failed with the status code '
                   '{1}.'.format(req, resp.status_code))
            raise Exception(msg)

        if resp.entity is None:
            if obj_id is None:
                msg = ('Response body for {0} did not deserialize as '
                       'expected.'.format(req))
            else:
                msg = ('Response body for {0} with the uuid {1} did not '
                       'deserialize as expected.'.format(req, obj_id))
            raise Exception(msg)

        return resp.entity
