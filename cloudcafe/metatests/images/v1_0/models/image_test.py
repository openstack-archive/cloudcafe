import re
from datetime import datetime
from unittest import TestCase

from cloudcafe.images.v1_0.models.image import Image
from cloudcafe.images.v1_0.models.member import Member


class ImageTest(TestCase):
    """@summary: Testing the behaviors of the image model..."""

    @classmethod
    def setUp(self):
        self.raw_str = '{"images": ' \
                       '[{"status": "active", ' \
                       '"name": "precise", ' \
                       '"deleted": false, ' \
                       '"container_format": "bare", ' \
                       '"created_at": "2013-04-29T19:32:56", ' \
                       '"disk_format": "qcow2", ' \
                       '"updated_at": "2013-04-29T19:32:56", ' \
                       '"properties": {}, ' \
                       '"min_disk": 0, ' \
                       '"protected": false, ' \
                       '"id": "46fd5b5c-b925-4316-a878-63cbbe7f0030", ' \
                       '"checksum": null, ' \
                       '"owner": "bd7531a57d3a47538fae1b89c169b293", ' \
                       '"is_public": true, ' \
                       '"deleted_at": null, ' \
                       '"min_ram": 0, ' \
                       '"size": 252116992}]}'

        self.image_one = Image(
            id="46fd5b5c-b925-4316-a878-63cbbe7f0030",
            status="active",
            name="precise",
            deleted=False,
            container_format="bare",
            created_at=datetime.strptime("2013-04-29T19:32:56",
                                         '%Y-%m-%dT%H:%M:%S'),
            disk_format="qcow2",
            updated_at=datetime.strptime("2013-04-29T19:32:56",
                                         '%Y-%m-%dT%H:%M:%S'),
            owner="bd7531a57d3a47538fae1b89c169b293",
            protected=False,
            min_ram=0,
            checksum=None,
            min_disk=0,
            is_public=True,
            deleted_at=None,
            properties={},
            size=252116992)

        self.image_two = Image(
            id="c7dd539e-5077-49e8-bc4d-0359ba051122",
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

        self._dict = {
            'id': self.image_one.id,
            'status': self.image_one.status,
            'name': self.image_one.name,
            'deleted': self.image_one.deleted,
            'container_format': self.image_one.container_format,
            'created_at': "2013-04-29T19:32:56",
            'disk_format': self.image_one.disk_format,
            'updated_at': "2013-04-29T19:32:56",
            'owner': self.image_one.owner,
            'protected': self.image_one.protected,
            'min_ram': self.image_one.min_ram,
            'checksum': self.image_one.checksum,
            'min_disk': self.image_one.min_disk,
            'is_public': self.image_one.is_public,
            'deleted_at': self.image_one.deleted_at,
            'properties': self.image_one.properties,
            'size': self.image_one.size
        }

    def test_positive_equality_of_images(self):
        assert self.image_one == self.image_one
        assert not self.image_one == (self.image_two)

    def test_negative_equality_of_images(self):
        assert self.image_one != self.image_two
        assert not self.image_one != self.image_one

    def test_dict_to_image(self):
        assert Image._dict_to_obj(self._dict) == self.image_one

    def test_image_string_representations(self):
        regex = r"""(?x)\[(\s?\w*\:\s(\d{4}-\d{2}-\d{2}\s\d{2}:
            \d{2}:\d{2}\.\d{6}|[\w\d\-\{\}]*)\,?)*\s\]"""
        matches = re.match(regex, self.image_one.__repr__())
        assert matches is not None

    def test_json_to_image(self):
        assert len(Image._json_to_obj(self.raw_str)) == 1
        assert Image._json_to_obj(self.raw_str)[0] == self.image_one

    def test_add_member_to_an_image(self):
        member1 = Member(member_id='1')

        self.image_one.add_member(member1)

        assert len(self.image_one.members_list) == 1
        assert member1 in self.image_one.members_list

    def test_remove_member_from_an_image(self):
        member1 = Member(member_id='1')
        member2 = Member(member_id='2')

        self.image_one.add_member(member1)
        self.image_one.add_member(member2)
        assert len(self.image_one.members_list) == 2

        self.image_one.delete_member(member1)

        assert len(self.image_one.members_list) == 1
        assert member1 not in self.image_one.members_list
        assert member2 in self.image_one.members_list

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
