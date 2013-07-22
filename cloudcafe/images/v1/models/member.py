import json
from cafe.engine.models.base import \
    AutoMarshallingModel, AutoMarshallingListModel


class Member(AutoMarshallingModel):
    def __init__(self, member_id=None, shared_images=None, can_share=None):
        self.member_id = member_id
        self.shared_images = shared_images
        self.can_share = can_share

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)

        if 'members' in json_dict.keys():
            members = []
            members.extend([Member(**m) for m in json_dict['members']])
            return members
        else:
            return Member(**json_dict)


class MemberList(AutoMarshallingListModel):
    """Represent a list of Members"""

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)

        return [Member(**m) for m in json_dict.get('members')]
