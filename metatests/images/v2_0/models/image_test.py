import os
from copy import deepcopy
from datetime import datetime

from cloudcafe.images.common.types import ImageVisibility, \
    ImageStatus, ImageContainerFormat, ImageDiskFormat
from cloudcafe.images.v2.models.image import Image, Member


class TestImage(object):
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
        assert self.image_obj == deepcopy(self.image_obj)

    def test_negative_equality(self):
        different_obj = deepcopy(self.image_obj)
        different_obj.name = 'cirros-fake'

        assert self.image_obj != different_obj

    def test_deserialization_from_json(self):
        deserialized_obj = Image._json_to_obj(self.raw_image_str)

        assert self.image_obj == deserialized_obj

    def test_dict_to_obj(self):
        obj_dict = deepcopy(self.image_obj.__dict__)
        obj_dict['created_at'] = '2013-05-22T14:24:36Z'
        obj_dict['updated_at'] = '2013-05-22T14:24:36Z'
        obj_dict['id'] = obj_dict.pop('id_')
        obj_dict['self'] = obj_dict.pop('self_')
        obj_dict['file'] = obj_dict.pop('file_')
        image_obj = Image._dict_to_obj(obj_dict)

        assert self.image_obj == image_obj

    def test_serialization_to_json(self):
        serialized_obj = self.image_obj._obj_to_json()
        # we do this to overcome the property ordering:
        deserialized_obj = Image._json_to_obj(serialized_obj)

        assert set(self.image_obj.__dict__) == set(deserialized_obj.__dict__)
