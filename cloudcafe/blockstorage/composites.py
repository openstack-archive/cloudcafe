import warnings

from cloudcafe.auth.provider import MemoizedAuthServiceComposite
from cloudcafe.blockstorage.config import \
    BlockStorageConfig, BlockstorageAltUserConfig
from cloudcafe.blockstorage.volumes_api.common.config import VolumesAPIConfig

from cloudcafe.blockstorage.volumes_api.v1.config import \
    VolumesAPIConfig as v1Config
from cloudcafe.blockstorage.volumes_api.v1.client import \
    VolumesClient as v1Client
from cloudcafe.blockstorage.volumes_api.v1.behaviors import \
    VolumesAPI_Behaviors as v1Behaviors

from cloudcafe.blockstorage.volumes_api.v2.config import \
    VolumesAPIConfig as v2Config
from cloudcafe.blockstorage.volumes_api.v2.client import \
    VolumesClient as v2Client
from cloudcafe.blockstorage.volumes_api.v2.behaviors import \
    VolumesAPI_Behaviors as v2Behaviors


class _BlockstorageAuthComposite(MemoizedAuthServiceComposite):
    _blockstorage_config = BlockStorageConfig

    def __init__(self, endpoint_config=None, user_config=None):
        self._endpoint_config = endpoint_config
        self._user_config = user_config
        self.config = self._blockstorage_config()
        self.availability_zone = self.config.availability_zone
        super(_BlockstorageAuthComposite, self).__init__(
            self.config.identity_service_name, self.config.region,
            endpoint_config=endpoint_config, user_config=user_config)


class _BaseVolumesComposite(object):
    _config = None
    _client = None
    _behaviors = None
    _auth = _BlockstorageAuthComposite

    @classmethod
    def spawn_alt_user_composite(cls):
        """This will return a new composite of the same version and
        configuration as the composite this method is being called from,
        except with the blockstorage_alt_user config info used in place of the
        default user config.
        """
        alt_config = BlockstorageAltUserConfig()
        return cls(auth_composite=cls._auth(user_config=alt_config))

    def __init__(self, auth_composite=None):
        self.auth = auth_composite or self._auth()
        self.config = self._config()
        self.service_endpoint = self.auth.public_url
        if self.auth.config.service_endpoint_override is not None:
            self.service_endpoint = "{url}/{tenant_id}".format(
                url=self.auth.config.service_endpoint_override,
                tenant_id=self.auth.tenant_id)
        self.client = self._client(
            url=self.service_endpoint,
            auth_token=self.auth.token_id,
            serialize_format=self.config.serialize_format,
            deserialize_format=self.config.deserialize_format)
        self.behaviors = self._behaviors(self.client)

        # For backwards compatibility (deprecated - see property below)
        self._blockstorage_auth = self.auth

    @property
    def blockstorage_auth(self):
        warnings.warn(
            "the 'blockstorage_auth' attribute of the VolumesComposite is "
            "deprecated.  Please use the 'auth' attribute instead",
            DeprecationWarning)
        return self._blockstorage_auth


class VolumesV1Composite(_BaseVolumesComposite):
    _config = v1Config
    _client = v1Client
    _behaviors = v1Behaviors


class VolumesV2Composite(_BaseVolumesComposite):
    _config = v2Config
    _client = v2Client
    _behaviors = v2Behaviors


class VolumesAutoComposite(object):
    def __new__(cls, auth_composite=None, version_under_test=None):
        config = VolumesAPIConfig()
        if config.version_under_test == "1":
            return VolumesV1Composite(auth_composite=auth_composite)
        if config.version_under_test == "2":
            return VolumesV2Composite(auth_composite=auth_composite)
        else:
            raise Exception(
                "VolumesAutoComposite cannot be used unless the "
                "'version_under_test' attribute of the VolumesAPIConfig"
                " is set to either '1' or '2'")
