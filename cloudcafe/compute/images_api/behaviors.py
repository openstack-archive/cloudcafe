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

import time

from cloudcafe.common.behaviors import StatusProgressionVerifier
from cloudcafe.common.tools.datagen import rand_name
from cloudcafe.compute.common.behaviors import BaseComputeBehavior
from cloudcafe.compute.common.types import NovaImageStatusTypes as ImageStates
from cloudcafe.compute.common.types import ComputeTaskStates
from cloudcafe.compute.common.exceptions import ItemNotFound, \
    TimeoutException, BuildErrorException


class ImageBehaviors(BaseComputeBehavior):

    def __init__(self, images_client, servers_client, config):
        super(ImageBehaviors, self).__init__()
        self.config = config
        self.images_client = images_client
        self.servers_client = servers_client

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
        @param interval_time: The amount of time in seconds to wait
                              before aborting
        @type interval_time: Integer
        @return: Response object containing response and the image
                 domain object
        @rtype: requests.Response
        """

        interval_time = interval_time or self.config.image_status_interval
        timeout = timeout or self.config.snapshot_timeout
        end_time = time.time() + timeout

        while time.time() < end_time:
            resp = self.images_client.get_image(image_id)
            image = resp.entity

            if image.status.lower() == ImageStates.ERROR.lower():
                raise BuildErrorException(
                    'Build failed. Image with UUID {0} '
                    'entered ERROR status.'.format(image.id))

            if image.status == desired_status:
                break
            time.sleep(interval_time)
        else:
            raise TimeoutException(
                "wait_for_image_status ran for {0} seconds and did not "
                "observe image {1} reach the {2} status.".format(
                    timeout, image_id, desired_status))

        return resp

    def wait_for_image_resp_code(self, image_id, response_code,
                                 interval_time=None, timeout=None):
        """
        @summary: Waits for a image to reach a desired status. Primarily
                  as a polling mechanism to determine when a new image
                  registers in Glance
        @param image_id: The uuid of the image
        @type image_id: String
        @param response_code: The desired response code
        @type response_code: String
        @param interval_time: The amount of time in seconds to wait
                              between polling
        @type interval_time: Integer
        @param interval_time: The amount of time in seconds to wait
                              before aborting
        @type interval_time: Integer
        @return: Response object containing response and the image
                 domain object
        @rtype: requests.Response
        """

        interval_time = interval_time or self.config.image_status_interval
        timeout = timeout or self.config.snapshot_timeout
        end_time = time.time() + timeout

        while time.time() < end_time:
            resp = self.images_client.get_image(image_id)
            if resp.status_code == response_code:
                break
            time.sleep(interval_time)
        else:
            raise TimeoutException(
                "wait_for_image_resp_code ran for {0} seconds and did not "
                "receive a response with status {1} for image {2}.".format(
                    timeout, response_code, image_id))
        return resp

    def create_image_with_defaults(self, server_id, name=None, metadata=None):
        """
        @summary: Waits for an image to be created successfully
        @param server_id: The uuid of the server the image was created from
        @type server_id: String
        @param name: The name of the image
        @type name: String
        @param metadata: Metadata to be associated with the image
        @type metadata: dict
        @return: Response object containing response and the image
                 domain object
        @rtype: requests.Response
        """

        if name is None:
            name = rand_name('image')
        response = self.servers_client.create_image(
            server_id, name, metadata)
        return response

    def verify_image_creation_progression(self, image_id):
        verifier = StatusProgressionVerifier(
            'image', image_id,
            lambda id_: self.verify_entity(
                self.images_client.get_image(id_)).status,
            image_id)

        verifier.set_global_state_properties(
            timeout=self.config.snapshot_timeout)

        verifier.add_state(
            expected_statuses=[ImageStates.SAVING],
            acceptable_statuses=[ImageStates.ACTIVE],
            error_statuses=[ImageStates.ERROR, ImageStates.DELETED],
            poll_rate=self.config.image_status_interval)

        verifier.add_state(
            expected_statuses=[ImageStates.ACTIVE],
            error_statuses=[ImageStates.ERROR, ImageStates.DELETED],
            poll_rate=self.config.image_status_interval)

        verifier.start()
        response = self.images_client.get_image(image_id)
        return self.verify_entity(response)

    def verify_server_snapshotting_progression(self, server_id):
        # Wait while the server is imaging
        verifier = StatusProgressionVerifier(
            'server', server_id,
            lambda id_: self.verify_entity(
                self.servers_client.get_server(id_)).task_state,
            server_id)

        verifier.set_global_state_properties(
            timeout=self.config.snapshot_timeout)
        verifier.add_state(
            expected_statuses=[ComputeTaskStates.IMAGE_SNAPSHOT],
            acceptable_statuses=[ComputeTaskStates.IMAGE_PENDING_UPLOAD,
                                 ComputeTaskStates.IMAGE_UPLOADING],
            poll_rate=self.config.image_status_interval)
        verifier.add_state(
            expected_statuses=[ComputeTaskStates.IMAGE_PENDING_UPLOAD],
            acceptable_statuses=[ComputeTaskStates.IMAGE_UPLOADING],
            error_statuses=[ComputeTaskStates.NONE],
            poll_rate=self.config.image_status_interval)
        verifier.add_state(
            expected_statuses=[ComputeTaskStates.IMAGE_UPLOADING],
            error_statuses=[ComputeTaskStates.NONE],
            poll_rate=self.config.image_status_interval)
        verifier.add_state(
            expected_statuses=[ComputeTaskStates.NONE],
            poll_rate=self.config.image_status_interval)
        verifier.start()

        response = self.servers_client.get_server(server_id)
        return self.verify_entity(response)

    def create_active_image(self, server_id, name=None, metadata=None):
        """
        @summary: Creates an image from a server and waits for
                  the image to become active
        @param server_id: The uuid of the image
        @type server_id: String
        @return: Response object containing response and the image
                 domain object
        @rtype: requests.Response
        """

        response = self.create_image_with_defaults(
            server_id, name, metadata)

        # Retrieve the image id from the response header
        image_id = response.headers['location'].rsplit('/')[-1]

        self.verify_server_snapshotting_progression(server_id)
        image = self.verify_image_creation_progression(image_id)
        return self.images_client.get_image(image.id)

    def create_active_backup(self, server_id, backup_type, backup_rotation):
        """
        @summary: Creates a backup from a server and waits for
                  the backup to become active
        @param server_id: The uuid of the server
        @type server_id: String
        @param backup_type: The type of the backup, either daily or weekly.
        @type backup_type: String
        @param backup_rotation: Number of backups to maintain.
        @type backup_type: Integer
        @return: Response object containing response and the image
                 domain object
        @rtype: requests.Response
        """

        name = rand_name('backup')
        resp = self.servers_client.create_backup(
            server_id, backup_type, backup_rotation, name)
        assert resp.status_code == 202

        # Retrieve the backup id from the response header
        backup_id = resp.headers['location'].rsplit('/')[-1]
        resp = self.wait_for_image_status(backup_id, ImageStates.ACTIVE)
        return resp

    def wait_for_image_to_be_deleted(self, image_id, interval_time=None,
                                     timeout=None):
        """
        @summary: Waits for an image to be deleted
        @param image_id: The uuid of the image
        @type image_id: String
        @param interval_time: The amount of time in seconds to wait
                              between polling
        @type interval_time: Integer
        @param interval_time: The amount of time in seconds to wait
                              before aborting
        @type interval_time: Integer
        """

        interval_time = interval_time or self.config.image_status_interval
        timeout = timeout or self.config.snapshot_timeout
        end_time = time.time() + timeout

        while time.time() < end_time:
            try:
                image = self.images_client.get_image(image_id).entity
            except ItemNotFound:
                break

            # If GET on deleted images is enabled, check for DELETED status
            if (self.config.can_get_deleted_image
                    and image.status == ImageStates.DELETED):
                break
            time.sleep(interval_time)
        else:
            raise TimeoutException(
                "wait_for_image_to_be_deleted ran for {0} seconds "
                "and did not observe image {1} reach the "
                "{2} status.".format(
                    timeout, image_id, ImageStates.DELETED))

    def read_non_inherited_metadata(self):
        """
        @summary: Returns the non inherited metadata
        @return: List for user data processing
        @rtype: List
        """
        if self.config.non_inherited_metadata_filepath is None:
            non_inherited_metadata = []
        else:
            with open(self.config.non_inherited_metadata_filepath, "r") \
                    as myfile:
                data = myfile.read()
            non_inherited_metadata = data.split(",")
        return non_inherited_metadata

    def get_image_ids_by_name(self, search_name):
        """
        @summary: Returns list of desired image ids
        @param search_name: Name for group of images for example Red Hat
        @type search_name: String
        @return: List of image ids
        @rtype: List
        """
        all_images = self.images_client.list_images_with_detail()

        if all_images.entity is None:
                raise Exception(
                    "Response entity of list images with detail was not set. "
                    "Response was: {0}".format(all_images.content))

        image_ids = []
        for image in all_images.entity:
            if search_name in image.name:
                image_ids.append(image.id)
        return image_ids
