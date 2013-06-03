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

import json
from datetime import datetime
from copy import deepcopy

from cafe.engine.models.base import AutoMarshallingModel
from cloudcafe.compute.common.equality_tools import EqualityTools
from cloudcafe.images.common.types import ImageStatus, ImageVisibility, \
    ImageContainerFormat, ImageDiskFormat


class SchemaElement:
    def __init__(self, name=None, properties=None, type_=None):
        self.name = name
        self.properties = properties
        self.type_ = type_

class ImagesSchema(AutoMarshallingModel):

    def __init__(self, kj):
        super(self, __init__)
