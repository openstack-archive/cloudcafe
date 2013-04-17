from cloudcafe.common.models.configuration import ConfigSectionInterface


class UserEndpointConfig(ConfigSectionInterface):

    SECTION_NAME = 'user_auth_endpoint'

    @property
    def endpoint(self):
        return self.get("endpoint")

    @property
    def strategy(self):
        return self.get("strategy")


class ComputeAdminEndpointConfig(ConfigSectionInterface):

    SECTION_NAME = 'compute_admin_auth_endpoint'

    @property
    def endpoint(self):
        return self.get("endpoint")

    @property
    def strategy(self):
        return self.get("strategy")