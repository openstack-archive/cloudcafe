import json

from cloudcafe.identity.v3.common.models.base import BaseIdentityModel

from cloudcafe.identity.v3.common.roles.models.responses import Roles
from cloudcafe.identity.v3.common.catalog.models.responses import Catalog
from cloudcafe.identity.v3.common.users.models.responses import User
from cloudcafe.identity.v3.common.projects.models.responses import Project


class AuthResponse(BaseIdentityModel):
    """
    Auth Response model
    """

    ROOT_TAG = 'token'

    def __init__(
            self, token=None, roles=None, catalog=None, user=None,
            issued_at=None, extras=None, methods=None, project=None,
            expires_at=None):
        super(AuthResponse, self).__init__(locals())

        self.token = token
        self.roles = roles
        self.catalog = catalog
        self.user = user
        self.project = project
        self.issued_at = issued_at
        self.extras = extras
        self.methods = methods
        self.expires_at = expires_at

    @classmethod
    def _dict_to_obj(cls, data):
        """
        @summary: Converting Dictionary Representation of AuthResponse object
            to AuthResponse object
        @return: AuthResponse object
        @param data: Dictionary Representation of AuthResponse object
        """
        if data is None:
            return None
        return cls(
            token=AuthResponseToken._dict_to_obj(data.get("token")),
            roles=Roles._dict_to_obj(data.get("roles") or []),
            user=User._dict_to_obj(data.get("user")),
            catalog=Catalog._dict_to_obj(data.get("catalog")) or [],
            issued_at=data.get("issued_at"),
            extras=data.get("extras"),
            methods=data.get("methods"),
            project=Project._dict_to_obj(data.get("project")),
            expires_at=data.get("expires_at"))

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """
        @summary: Converting JSON Representation of AuthResponse object
            to AuthResponse object
        @return: AuthResponse object
        @param serialized_str: JSON Representation of AuthResponse object
        """
        data = json.loads(serialized_str)
        return cls._dict_to_obj(data.get("access"))

    def get_service(self, name):
        for service in self.catalog:
            if service.name == name:
                return service
        return None


class AuthResponseToken(BaseIdentityModel):
    def __init__(self, roles=None):
        super(AuthResponseToken, self).__init__(locals())

    @classmethod
    def _dict_to_obj(cls, data):
        """
        @summary: Converting Dictionary Representation of AuthResponseToken
         object to AuthResponseToken object
        @return: AuthResponseToken object
        @param data: Dictionary Representation of AuthResponseToken object
        """
        if data is None:
            return None
        return cls(roles=Roles._dict_to_obj(data.get("roles")))
