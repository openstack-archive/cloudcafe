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
import cStringIO as StringIO

from cloudcafe.compute.images_api.behaviors import \
    ImageBehaviors as ImageAPIBehaviors
from cloudcafe.auth.config import UserAuthConfig
from cloudcafe.auth.provider import AuthProvider
from cloudcafe.identity.v2_0.tenants_api.client import \
    TenantsAPI_Client
from cloudcafe.images.config import ImagesConfig

from cloudcafe.images.common.types import ImageStatus
from cloudcafe.compute.common.exceptions import \
    TimeoutException, BuildErrorException


class ImageBehaviors(ImageAPIBehaviors):

    def __init__(self, images_client, config):
        super(ImageBehaviors, self).__init__(images_client,
                                             None,
                                             config)

        access_data = AuthProvider().get_access_data()
        self.tenants_client = TenantsAPI_Client(
            UserAuthConfig().auth_endpoint,
            access_data.token.id_,
            'json', 'json')

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
            resp = self.images_client.retrieve_metadata(image_id)
            image_id = resp.headers['x-image-meta-id']
            image_status = resp.headers['x-image-meta-status']

            if image_status == ImageStatus.ERROR:
                raise BuildErrorException(
                    'Build failed. Image with uuid {0} entered ERROR status.'
                    .format(image_id))

            if image_status == desired_status:
                break
            time.sleep(interval_time)
        else:
            raise TimeoutException(
                "wait_for_image_status ran for {0} seconds and did not "
                "observe the image achieving the {1} status.".format(
                    timeout, desired_status))

        return resp

    def _create_remote_image(self, name, container_format, disk_format):
        """
            Create new remote image.
            @return ID of the newly registered image
        """
        name = 'New Remote Image {0}'.format(name)

        response = self.images_client.add_image(
            name,
            None,
            image_meta_container_format=container_format,
            image_meta_disk_format=disk_format,
            image_meta_is_public=True,
            image_meta_location=ImagesConfig.remote_image)

        return response.entity.id_

    def _create_standard_image(cls, name, container_format, disk_format, size):
        """
            Create new standard image.
            @return ID of the newly registered image
        """
        image_data = StringIO.StringIO('*' * size)
        name = 'New Standard Image {0}'.format(name)

        response = cls.images_client.add_image(
            name,
            image_data,
            image_meta_container_format=container_format,
            image_meta_disk_format=disk_format,
            image_meta_is_public=True)

        return response.entity.id_

    def _get_all_tenant_ids(self):
        """
            Get a list of all tenants
            @return list of Tenant IDs
        """
        response = self.tenants_client.list_tenants()
        tenants = response.entity

        return [x.id_ for x in tenants]
