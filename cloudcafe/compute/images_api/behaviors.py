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

from cloudcafe.compute.common.datagen import rand_name
from cloudcafe.compute.common.types import NovaImageStatusTypes as ImageStates
from cloudcafe.compute.common.exceptions import ItemNotFound, \
    TimeoutException, BuildErrorException


class ImageBehaviors(object):

    def __init__(self, images_client, servers_client, config):

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
                    'Build failed. Image with uuid %s entered ERROR status.'
                    % image.id)

            if image.status == desired_status:
                break
            time.sleep(interval_time)
        else:
            raise TimeoutException(
                "wait_for_image_status ran for {0} seconds and did not "
                "observe the image achieving the {1} status.".format(
                    timeout, desired_status))

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
                "receive a response with status code {1}.".format(
                    timeout, response_code))
        return resp

    def create_active_image(self, server_id):
        """
        @summary: Creates an image from a server and waits for
                  the image to become active
        @param server_id: The uuid of the image
        @type server_id: String
        @return: Response object containing response and the image
                 domain object
        @rtype: requests.Response
        """

        name = rand_name('image')
        resp = self.servers_client.create_image(server_id, name)
        assert resp.status_code == 202

        # Retrieve the image id from the response header
        image_id = resp.headers['location'].rsplit('/')[-1]
        resp = self.wait_for_image_status(image_id, ImageStates.ACTIVE)
        return resp

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
            if self.config.can_get_deleted_image and image.status == ImageStates.DELETED:
                break
            time.sleep(interval_time)
        else:
            raise TimeoutException(
                "wait_for_image_to_be_deleted ran for {0} seconds "
                "and did not observe the image reaching the "
                "{1} status.".format(
                    timeout, ImageStates.DELETED))
