import os
import re
from copy import deepcopy
from datetime import datetime
from unittest import TestCase

from cloudcafe.images.common.types import ImageVisibility, \
    ImageStatus, ImageContainerFormat, ImageDiskFormat
from cloudcafe.images.v2_0.models.image import Image


class TestImage(TestCase):

    @classmethod
    def setup_class(cls):
        cls.raw_image_str = open(os.path.join(
            os.path.dirname(__file__), '../data/image.json')).read()
        cls.raw_images_str = open(os.path.join(
            os.path.dirname(__file__), '../data/images.json')).read()

        cls.image_obj = Image(
            id_='21c697d1-2cc5-4a45-ba50-61fab15ab9b7',
            name='cirros-0.3.1-x86_64-uec-ramdisk',
            visibility=ImageVisibility.PUBLIC,
            status=ImageStatus.ACTIVE,
            protected=False,
            tags=[],
            checksum='69c33642f44ca552ba4bb8b66ad97e85',
            size=3714968,
            created_at=datetime.strptime('2013-05-22T14:24:36Z',
                                         '%Y-%m-%dT%H:%M:%SZ'),
            updated_at=datetime.strptime('2013-05-22T14:24:36Z',
                                         '%Y-%m-%dT%H:%M:%SZ'),
            file_='/v2/images/21c697d1-2cc5-4a45-ba50-61fab15ab9b7/file',
            self_='/v2/images/21c697d1-2cc5-4a45-ba50-61fab15ab9b7',
            schema='/v2/schemas/image',
            container_format=ImageContainerFormat.ARI,
            disk_format=ImageDiskFormat.ARI,
            min_disk=0,
            min_ram=0
        )

    def test_positive_equality(self):
        duplicate_obj = deepcopy(self.image_obj)
        assert duplicate_obj == self.image_obj

    def test_negative_equality(self):
        different_obj = deepcopy(self.image_obj)
        different_obj.created_at = datetime.now()
        different_obj.updated_at = datetime.now()
        different_obj.name = 'cirros-fake'

        assert different_obj != self.image_obj

    def test_string_representation(self):
        """
            Tests whether string representation
            conforms to the following format:

            ['status: ACTIVE',
            'id_: 21c697d1-2cc5-4a45-ba50-61fab15ab9b7',
            'name: cirros-0.3.1-x86_64-uec-ramdisk',
            'tags: []',
            'checksum: 69c33642f44ca552ba4bb8b66ad97e85',
            'created_at: 2013-05-22T14:24:36Z',
            'file_: /v2/images/21c697d1-2cc5-4a45-ba50-61fab15ab9b7/file',
            'updated_at: 2013-05-22T14:24:36Z',
            'visibility: PUBLIC',
            'self_: /v2/images/21c697d1-2cc5-4a45-ba50-61fab15ab9b7',
            'protected: False',
            'container_format: ARI',
            'min_disk: 0',
            'schema: /v2/schemas/image',
            'disk_format: ARI',
            'min_ram: 0',
            'size: 3714968']
        """
        regex = r'''(?x)\[(\s*\'[a-z_]*:\s
            (\d{4}-\d{2}-\d{2}[T]\d{2}:\d{2}:\d{2}[Z]|
            [a-zA-Z0-9\-\.\_\[\]\/]*)\',?)*]'''
        matches = re.match(regex, self.image_obj.__repr__())
        assert matches is not None

    def test_deserialization_from_json(self):
        deserialized_obj = Image._json_to_obj(self.raw_image_str)

        print self.image_obj
        print deserialized_obj
        assert self.image_obj == deserialized_obj

    def test_serialization_to_json(self):
        serialized_obj = self.image_obj._obj_to_json()
        # we do this to overcome the property ordering:
        deserialized_obj = Image._json_to_obj(serialized_obj)

        assert self.image_obj == deserialized_obj
