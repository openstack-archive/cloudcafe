import cloudcafe.identity.v3 as lib_pt
import fnmatch
import importlib
import os

from cloudcafe.identity.common.client import BaseIdentityAPIClient
from cloudcafe.identity.v3.config import (
    ServiceAdmin, UserAdmin, DefaultUser, Roles)
from cloudcafe.identity.v3.config import IdentityV3Config
from cloudcafe.identity.v3.common.tokens.behavior import TokensBehavior
from cloudcafe.identity.v3.common.tokens.client import TokensClient


class IdentityV3Composite(object):
    _user_config_class = UserAdmin
    _ident_config_class = IdentityV3Config

    def __init__(self, user_config=None):
        self.ident_config = self._ident_config_class()
        self.service_admin = ServiceAdmin()
        self.default_user = DefaultUser()
        self.roles = Roles()
        self.user_config = (user_config() if user_config else
                            self._user_config_class())

        self.user_type = self.user_config.SECTION_NAME
        self.url = (
            self.user_config.authentication_endpoint or
            self.ident_config.global_authentication_endpoint)
        self.tokens_client = TokensClient(
            url=self.url,
            serialize_format=self.ident_config.serialize_format,
            deserialize_format=self.ident_config.deserialize_format,
            auth_token=None)
        self.tokens_behavior = TokensBehavior(self.tokens_client)
        self.load_clients_and_behaviors()

    def load_clients_and_behaviors(self):
        """
        @summary Recursively loads client and behaviors as specified in the
        __init__.py files.
        """
        self.fetch_token()
        kwargs = {
            "url": self.url,
            "serialize_format": self.ident_config.serialize_format,
            "deserialize_format": self.ident_config.deserialize_format,
            "auth_token": self.token}
        self.apis = APINamespace()

        # get_modules_within will get the __init__.py's from the
        # subdirectories. It then loads those and gets the client or behavior
        # that is set within the __init__.py
        for name, module in self.get_modules_within(lib_pt).iteritems():
            module_path = "{path}.{module}".format(
                path=lib_pt.__name__, module=module)
            module = module.replace("common.", "")
            package = importlib.import_module(module_path)
            client_class = getattr(package, "client", None)
            behavior_class = getattr(package, "behavior", None)
            if (not isinstance(client_class, type) or
                    not issubclass(client_class, BaseIdentityAPIClient)):
                continue
            client = client_class(**kwargs)
            setattr(self.apis, module, APIComposite(client, behavior_class))

    def fetch_token(self):
        """
        Authenticate and retrieve the resp and the token in the header
        """
        resp = self.tokens_behavior.authenticate(
            username=self.user_config.username,
            password=self.user_config.password)
        self.access_data = resp.entity
        self.token = resp.headers['x-subject-token']
        return resp

    def get_modules_within(self, library):
        """
        @summary This method finds all submodules and returns a dictionary
        For example common/catalog/client.py would be become this map:
        catalog : common.catalog.client
        """
        path = os.path.dirname(library.__file__)
        file_type = "__init__.py"

        # This will loop through all subdirectories of the specified
        # module for __init__.py files
        modules = [os.path.join(dirpath, f)
                   for dirpath, dirnames, files in os.walk(path)
                   for f in fnmatch.filter(files, file_type)]

        # get the module names + .py from the path, then remove the .py
        modules = [x.split(path)[1].lstrip('/') for x in modules if path in x]
        modules = [x.strip(file_type) for x in modules]

        # convert the forward slashes to .'s
        modules = [x.rstrip('/').replace('/', '.') for x in modules if x != '']

        # build up a hash list mapping module name to the module path
        return dict([(x.split('.')[-1], x) for x in modules])


class APINamespace(object):
    pass


class APIComposite(object):
    def __init__(self, client, behavior=None):
        self.client = client
        if behavior is not None:
            self.behavior = behavior(client)
