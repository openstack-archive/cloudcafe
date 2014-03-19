from cloudcafe.identity.v2_0.behaviors import IdentityServiceBehaviors
from cloudcafe.identity.v2_0.client import IdentityServiceClient
from cloudcafe.identity.v2_0.config import (
    IdentityConfig, IdentityUserConfig, IdentityAdminConfig)
from cloudcafe.identity.v2_0.extensions import osksadm


class IdentityServiceComposite(object):
    _user_config_class = IdentityUserConfig

    def __init__(self):
        ident_config = IdentityConfig()
        user_config = self._user_config_class()
        self.serialize_format = ident_config.serialize_format
        self.deserialize_format = ident_config.deserialize_format
        self.config_token = ident_config.token_id
        self.service_name = ident_config.identity_service_name
        self.region = ident_config.region
        self.username = user_config.username
        self.password = user_config.password
        self.tenant_name = user_config.tenant_name
        self.config_tenant_id = user_config.tenant_id
        self.endpoint = user_config.authentication_endpoint

        self.client = IdentityServiceClient(
            url=self.endpoint, serialize_format=self.serialize_format,
            deserialize_format=self.deserialize_format)
        self.behaviors = IdentityServiceBehaviors(
            self.client)
        self.public_url = None
        self.private_url = None
        self.admin_url = None

    def authenticate(self):
        resp = IdentityServiceBehaviors.memoized_authenticate(
            self.username, self.password, self.tenant_name, self.client.url,
            self.serialize_format, self.deserialize_format)
        if resp.entity is None:
            raise Exception("Failed to authenticate")
        self.access_data = resp.entity
        self.client.token = self.access_data.token.id_
        self.user_id = self.access_data.user.id_
        self.tenant_id = self.access_data.token.tenant.id_
        service = self.access_data.get_service(self.service_name)
        endpoint = service.get_endpoint(self.region)
        self.public_url = endpoint.public_url
        self.private_url = endpoint.private_url
        self.admin_url = endpoint.admin_url

    def load_extensions(self):
        self.extensions = ExtensionsComposite(self.endpoint, self.client.token)


class AdminIdentityServiceComposite(IdentityServiceComposite):
    _user_config_class = IdentityAdminConfig


class ExtensionsComposite():
    extensions = {}

    def __init__(self, url, auth_token):
        for ext in self.extensions:
            composite = self.extensions.get(ext)(url, auth_token)
            setattr(self, ext, composite)


class ExtensionType(type):
    def __new__(cls, cls_name, cls_parents, cls_attr):
        new_class = super(ExtensionType, cls).__new__(
            cls, cls_name, cls_parents, cls_attr)
        if getattr(new_class, "_name", False):
            ExtensionsComposite.extensions[new_class._name] = new_class
        return new_class


class BaseIdentityExtensionComposite(object):
    _client = None
    _behaviors = None
    _name = None
    __metaclass__ = ExtensionType

    def __init__(self, url, auth_token):
        config = IdentityConfig()
        self.client = self._client(
            url=url, auth_token=auth_token,
            serialize_format=config.serialize_format,
            deserialize_format=config.deserialize_format)
        if self._behaviors is not None:
            self.behaviors = self._behaviors(self.client)


#All Extension Composites below this point
class OSKSADMComposite(BaseIdentityExtensionComposite):
    _client = osksadm.client
    _behaviors = osksadm.behaviors
    _name = "osksadm"
