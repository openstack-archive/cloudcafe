from cloudcafe.auth.provider import MemoizedAuthServiceComposite
from cloudcafe.blockstorage.config import BlockStorageConfig
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
    def __init__(self):
        self.config = BlockStorageConfig()
        self.availability_zone = \
            self.config.availability_zone
        super(_BlockstorageAuthComposite, self).__init__(
            self.config.identity_service_name, self.config.region)


class _BaseVolumesComposite(object):
    _config = None
    _client = None
    _behaviors = None

    def __init__(self):
        self.blockstorage_auth = _BlockstorageAuthComposite()
        self.config = self._config()
        self.client = self._client(
            url=self.blockstorage_auth.public_url,
            auth_token=self.blockstorage_auth.token_id,
            serialize_format=self.config.serialize_format,
            deserialize_format=self.config.deserialize_format)
        self.behaviors = self._behaviors(self.client)


#For version specific tests
class VolumesV1Composite(_BaseVolumesComposite):
    _config = v1Config
    _client = v1Client
    _behaviors = v1Behaviors


class VolumesV2Composite(_BaseVolumesComposite):
    _config = v2Config
    _client = v2Client
    _behaviors = v2Behaviors


#For version agnostic tests
class VolumesAutoComposite(object):
    def __new__(cls):
        config = VolumesAPIConfig()
        if config.version_under_test == "1":
            return VolumesV1Composite()
        if config.version_under_test == "2":
            return VolumesV2Composite()
        else:
            raise Exception(
                "VolumesAutoComposite cannot be used unless the "
                "'version_under_test' attribute of the VolumesAPIConfig"
                " is set to either '1' or '2'")
