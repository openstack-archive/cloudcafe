from datetime import datetime
from cloudcafe.images.v2.models.image import Member


class TestMember(object):
    @classmethod
    def setup_class(cls):
        cls.raw_member_str = ('''{
            "status": "accepted",
            "created_at": "2013-09-17T12:51:03Z",
            "updated_at": "2013-09-17T13:14:28Z",
            "image_id": "af61731b-7181-4831-821f-b868df122f5a",
            "member_id": "someguy",
            "schema": "/v2/schemas/member"
        }''')

        cls.member_obj = \
            Member(member_id='someguy', status='accepted',
                   created_at=datetime.strptime('2013-09-17T12:51:03Z',
                                                '%Y-%m-%dT%H:%M:%SZ'),
                   updated_at=datetime.strptime('2013-09-17T13:14:28Z',
                                                '%Y-%m-%dT%H:%M:%SZ'),
                   image_id='af61731b-7181-4831-821f-b868df122f5a')

    def test_json_to_obj(self):
        deserialized_obj = Member._json_to_obj(self.raw_member_str)

        assert self.member_obj == deserialized_obj
