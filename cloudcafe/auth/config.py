from cloudcafe.common.models.configuration import ConfigSectionInterface


class UserAuthConfig(ConfigSectionInterface):

    SECTION_NAME = 'user_auth_config'

    @property
    def auth_endpoint(self):
        return self.get("endpoint")

    @property
    def strategy(self):
        return self.get("strategy")


class ComputeAdminAuthConfig(UserAuthConfig):

    SECTION_NAME = 'compute_admin_auth_config'


class UserConfig(ConfigSectionInterface):

    SECTION_NAME = 'user'

    @property
    def username(self):
        return self.get("username")

    @property
    def api_key(self):
        return self.get_raw("api_key")

    @property
    def password(self):
        return self.get_raw("password")

    @property
    def tenant_id(self):
        return self.get("tenant_id")

    @property
    def tenant_name(self):
        return self.get("tenant_name")


class ComputeAuthorizationConfig(UserConfig):

    SECTION_NAME = 'compute_secondary_user'


class ComputeAdminUserConfig(UserConfig):

    SECTION_NAME = 'compute_admin_user'
