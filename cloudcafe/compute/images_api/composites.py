"""
Copyright 2014 Rackspace

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

from cloudcafe.compute.common.composites import BaseComputeComposite
from cloudcafe.compute.images_api.behaviors import ImageBehaviors
from cloudcafe.compute.images_api.client import ImagesClient
from cloudcafe.compute.images_api.config import ImagesConfig


class ImagesComposite(BaseComputeComposite):
    behavior_class = ImageBehaviors

    def __init__(self, auth_composite):
        super(ImagesComposite, self).__init__(auth_composite)
        self.config = ImagesConfig()
        self.client = ImagesClient(**self.compute_auth_composite.client_args)
        self.behaviors = None
