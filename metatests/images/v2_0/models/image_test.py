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

from copy import deepcopy
import dateutil.parser
import json
import os
import unittest2 as unittest

from cloudcafe.images.common.types import (
    ImageContainerFormat, ImageDiskFormat, ImageStatus, ImageVisibility)
from cloudcafe.images.v2.models.image import Image


class TestImage(unittest.TestCase):

    @classmethod
    def setup_class(cls):
        cls.raw_image_str = open(os.path.join(
            os.path.dirname(__file__), '../data/image.json')).read()
        cls.raw_images_str = open(os.path.join(
            os.path.dirname(__file__), '../data/images.json')).read()

        # Required due to datetime parser in image client
        date_time = dateutil.parser.parse(unicode('2013-05-22T14:24:36Z'))

        cls.image_obj = Image(
            checksum='69c33642f44ca552ba4bb8b66ad97e85',
            container_format=ImageContainerFormat.ARI,
            created_at=date_time,
            disk_format=ImageDiskFormat.ARI,
            file_='/v2/images/21c697d1-2cc5-4a45-ba50-61fab15ab9b7/file',
            id_='21c697d1-2cc5-4a45-ba50-61fab15ab9b7',
            min_disk=0,
            min_ram=0,
            name='cirros-0.3.1-x86_64-uec-ramdisk',
            protected=False,
            schema='/v2/schemas/image',
            self_='/v2/images/21c697d1-2cc5-4a45-ba50-61fab15ab9b7',
            size=3714968,
            status=ImageStatus.ACTIVE,
            tags=[],
            updated_at=date_time,
            visibility=ImageVisibility.PUBLIC,
            additional_properties={unicode('additional_properties'): {}})

        cls.obj_dict = json.loads(cls.raw_image_str)

    def test_positive_equality(self):
        assert self.image_obj == deepcopy(self.image_obj)

    def test_negative_equality(self):
        different_obj = deepcopy(self.image_obj)
        different_obj.name = 'cirros-fake'
        assert self.image_obj != different_obj

    def test_deserialization_from_json(self):
        deserialized_obj = Image._json_to_obj(self.raw_image_str)
        assert self.image_obj == deserialized_obj

    def test_dict_to_obj(self):
        assert self.image_obj == Image._dict_to_obj(self.obj_dict)

    def test_serialization_to_json(self):
        # Required due to datetime parser in image client
        setattr(self.image_obj, 'created_at', '2013-05-22T14:24:36Z')
        setattr(self.image_obj, 'updated_at', '2013-05-22T14:24:36Z')
        serialized_obj = self.image_obj._obj_to_json()
        # we do this to overcome the property ordering:
        deserialized_obj = Image._json_to_obj(serialized_obj)

        assert set(self.image_obj.__dict__) == set(deserialized_obj.__dict__)
