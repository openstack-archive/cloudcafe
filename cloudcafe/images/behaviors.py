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


class ImagesBehaviors(object):
    """
    @summary: Base Behaviors class for having common methods for V1 and V2 api
    For example: is_valid_image_status(image.status) method is common for 
    image model response returned from v1 and v2 api calls.
    """

    def __init__(self, config):
        self.config = config
