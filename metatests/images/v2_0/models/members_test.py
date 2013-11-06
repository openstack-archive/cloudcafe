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

import dateutil

from cloudcafe.images.v2.models.image import Members, Member


class TestMembers(object):
    @classmethod
    def setup_class(cls):
        cls.raw_members_str = ('''{
        "members": [
        {
            "status": "accepted",
            "created_at": "2013-09-17T12:51:03Z",
            "updated_at": "2013-09-17T13:14:28Z",
            "image_id": "af61731b-7181-4831-821f-b868df122f5a",
            "member_id": "someguy",
            "schema": "/v2/schemas/member"
        }],
        "schema": "/v2/schemas/members"
        }''')

        cls.members_obj = [(
            Member(member_id='someguy', status='accepted',
                   created_at=dateutil.parser.parse('2013-09-17T12:51:03Z'),
                   updated_at=dateutil.parser.parse('2013-09-17T13:14:28Z'),
                   image_id='af61731b-7181-4831-821f-b868df122f5a'))]

    def test_json_to_obj(self):
        deserialized_obj = Members._json_to_obj(self.raw_members_str)

        assert self.members_obj == deserialized_obj
