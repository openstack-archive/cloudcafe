from ast import literal_eval

from cafe.engine.models.data_interfaces import ConfigSectionInterface


class IdentityConfig(ConfigSectionInterface):

    SECTION_NAME = 'identity'

    @property
    def serialize_format(self):
        return self.get("serialize_format", "json")

    @property
    def deserialize_format(self):
        return self.get("deserialize_format", "json")

    @property
    def global_authentication_endpoint(self):
        return self.get("global_authentication_endpoint")

    @property
    def environment(self):
        return literal_eval(self.get("environment"))


class IdentityUserConfig(ConfigSectionInterface):

    SECTION_NAME = 'Base class do not use'

    @property
    def username(self):
        return self.get("username")

    @property
    def password(self):
        return self.get("password")

    @property
    def user_id(self):
        return self.get("user_id")

    @property
    def domain_id(self):
        return self.get("domain_id")

    @property
    def domain_name(self):
        return self.get("domain_name")

    @property
    def project_id(self):
        return self.get("project_id")

    @property
    def project_name(self):
        return self.get("project_name")

    @property
    def role_id(self):
        return self.get("role_id")

    @property
    def role_name(self):
        return self.get("role_name")

    @property
    def authentication_endpoint(self):
        """This overrides the global_authentication_endpoint in composite"""
        return self.get("authentication_endpoint")


class Roles(ConfigSectionInterface):

    SECTION_NAME = 'roles'

    @property
    def compute_role_id(self):
        return self.get("compute_role_id")

    @property
    def compute_role_name(self):
        return self.get("compute_role_name")

    @property
    def object_store_role_id(self):
        return self.get("object_store_role_id")

    @property
    def object_store_role_name(self):
        return self.get("object_store_role_name")

    @property
    def nast_prefix(self):
        return self.get("nast_prefix")


class ServiceAdmin(IdentityUserConfig):
    SECTION_NAME = 'service_admin'


class IdentityAdmin(IdentityUserConfig):
    SECTION_NAME = 'identity_admin'


class UserAdmin(IdentityUserConfig):
    SECTION_NAME = 'user_admin'


class UserManage(IdentityUserConfig):
    SECTION_NAME = 'user_manage'


class DefaultUser(IdentityUserConfig):
    SECTION_NAME = 'default_user'


class OneUser(IdentityUserConfig):
    SECTION_NAME = 'one_user'
