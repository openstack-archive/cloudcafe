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
