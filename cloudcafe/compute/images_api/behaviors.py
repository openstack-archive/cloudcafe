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

from cloudcafe.compute.common.types import NovaImageStatusTypes as ImageStates
from cloudcafe.compute.common.exceptions import ItemNotFound, \
    TimeoutException, BuildErrorException


class ImageBehaviors(object):

    def __init__(self, images_client, config):

        self.config = config
        self.images_client = images_client


    def wait_for_image_status(self, image_id, desired_status):
        '''Polls image image_id details until status_to_wait_for is met.'''
        image_response = self.images_client.get_image(image_id)
        image_obj = image_response.entity
        time_waited = 0
        interval_time = self.config.image_status_interval
        while (image_obj.status.lower() != desired_status.lower() and
                       time_waited < self.config.snapshot_timeout):
            image_response = self.images_client.get_image(image_id)
            image_obj = image_response.entity

            if image_obj.status.lower() is ImageStates.ERROR.lower():
                message = 'Snapshot failed. Image with uuid {0} entered ERROR status.'
                raise BuildErrorException(message.format(image_id))

            time.sleep(interval_time)
            time_waited += interval_time
        return image_response

    def wait_for_image_resp_code(self, image_id, response_code):
        '''Polls image resp for the specified status code.'''

        image_response = self.images_client.get_image(image_id)
        image_obj = image_response.entity
        time_waited = 0
        interval_time = self.config.image_status_interval
        while (image_response.status_code != response_code and
                       image_obj.status.lower() != ImageStates.ERROR.lower() and
                       time_waited < self.config.snapshot_timeout):
            image_response = self.images_client.get_image(image_id)
            image_obj = image_response.entity
            time.sleep(interval_time)
            time_waited += interval_time
        return image_response

    def wait_for_image_to_be_deleted(self, image_id):
        '''Waits for the image to be deleted. '''

        image_response = self.images_client.delete_image(image_id)
        image_obj = image_response.entity
        time_waited = 0
        interval_time = self.config.image_status_interval

        try:
            while (True):
                image_response = self.images_client.get_image(image_id)
                image_obj = image_response.entity
                if time_waited > self.config.snapshot_timeout:
                    raise TimeoutException("Timed out while deleting image id: %s" % image_id)
                if image_obj.status.lower() == ImageStates.DELETED.lower():
                    return
                if image_obj.status.lower() != ImageStates.ERROR.lower():
                    raise BuildErrorException("Image entered Error state while deleting, Image id : %s" % image_id)
                time.sleep(interval_time)
                time_waited += interval_time
        except ItemNotFound:
            pass