import json
import os
from copy import deepcopy
from datetime import datetime

from cloudcafe.images.v1.models.image import Image
from cloudcafe.images.v1.models.member import Member


class TestImage(object):
    """@summary: Testing the behaviors of the image model..."""

    @classmethod
    def setup_class(cls):
        cls.raw_image_str = open(os.path.join(
            os.path.dirname(__file__), '../data/image.json')).read()
        cls.raw_images_str = open(os.path.join(
            os.path.dirname(__file__), '../data/images.json')).read()

        cls._dict = json.loads(cls.raw_image_str).get('image')

        cls.image_one = Image(
            id_=cls._dict.get('id'),
            name=cls._dict.get('name'),
            container_format=cls._dict.get('container_format'),
            checksum=cls._dict.get('checksum'),
            size=cls._dict.get('size'),
            disk_format=cls._dict.get('disk_format'))

        cls.image_two = Image(
            id_="c7dd539e-5077-49e8-bc4d-0359ba051122",
            status="active",
            name="precise",
            deleted="False",
            container_format="cirros",
            created_at=datetime.today(),
            disk_format="qcow2",
            updated_at=datetime.today(),
            owner="bd7531a57d3a47538fae1b89c169b293",
            protected="False",
            min_ram=0,
            checksum="",
            min_disk=0,
            is_public="True",
            deleted_at=datetime.today(),
            properties={},
            size=252116992)

    def test_positive_equality_of_images(self):
        assert self.image_one == deepcopy(self.image_one)

    def test_negative_equality_of_images(self):
        assert self.image_one != deepcopy(self.image_two)

    def test_dict_to_obj(self):
        assert Image._dict_to_obj(self._dict) == self.image_one

    def test_json_to_obj(self):
        assert Image._json_to_obj(self.raw_image_str) == self.image_one

    def test_add_member_to_an_image(self):
        member1 = Member(member_id='1')

        self.image_one.add_member(member1)

        assert len(self.image_one.members_list) == 1
        assert member1 in self.image_one.members_list

    def test_remove_member_from_an_image(self):
        image = Image._dict_to_obj(self._dict)
        member1 = Member(member_id='1')
        member2 = Member(member_id='2')

        image.add_member(member1)
        image.add_member(member2)
        assert len(image.members_list) == 2

        image.delete_member(member1)

        assert len(image.members_list) == 1
        assert member1 not in image.members_list
        assert member2 in image.members_list

    def test_replace_members_list_for_an_image(self):
        member1 = Member(member_id='1')
        member2 = Member(member_id='2')
        member3 = Member(member_id='3')

        members_list = [member1, member2]
        image = self.image_one
        image.members_list = members_list

        image.replace_members_list([member3])

        assert len(image.members_list) == 1
        assert member1 not in image.members_list
        assert member2 not in image.members_list
        assert member3 in image.members_list
