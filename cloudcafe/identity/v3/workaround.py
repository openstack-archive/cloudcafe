from cafe.engine.behaviors import BaseBehavior
from syntribos.extensions.identity import client

from cloudcafe.identity.common.models.base import BaseIdentityModel


class AuthResponse(BaseIdentityModel):
    def __init__(self, token=None):
        self.token = token

    @classmethod
    def _dict_to_obj(cls, dict_):
        return cls(TokenResponse._dict_to_obj(dict_.get("token")))


class TokenResponse(BaseIdentityModel):
    def __init__(self, id_=None):
        self.id_ = id_

    @classmethod
    def _dict_to_obj(cls, dict_):
        return cls(dict_.get("user").get("id"))


class IdentityV3Behavior(BaseBehavior):
    @staticmethod
    def get_access_data(username, password, url, domain_name="default"):
        r = client.authenticate_v3(
            url, username, password, domain_name=domain_name)
        return AuthResponse._json_to_obj(r.content)

