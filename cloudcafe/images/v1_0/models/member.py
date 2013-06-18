from cafe.engine.models.base import AutoMarshallingModel


class Member(AutoMarshallingModel):
    def __init__(self, member_id=None, shared_images=None):
        self.member_id = member_id
        self.shared_images = shared_images
