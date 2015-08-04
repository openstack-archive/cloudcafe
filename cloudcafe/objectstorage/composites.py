from cloudcafe.auth.provider import MemoizedAuthServiceComposite
from cloudcafe.objectstorage.config import ObjectStorageConfig
from cloudcafe.objectstorage.objectstorage_api.behaviors \
    import ObjectStorageAPI_Behaviors
from cloudcafe.objectstorage.objectstorage_api.client \
    import ObjectStorageAPIClient
from cloudcafe.objectstorage.objectstorage_api.config \
    import ObjectStorageAPIConfig


class _ObjectStorageAuthComposite(MemoizedAuthServiceComposite):
    def __init__(self):
        self.config = ObjectStorageConfig()

        super(_ObjectStorageAuthComposite, self).__init__(
            self.config.identity_service_name, self.config.region)


class ObjectStorageComposite(object):
    """
    Handles authing and retrieving the storage_url and auth_token for
    storage objects.
    """
    _auth_composite = _ObjectStorageAuthComposite

    def __init__(self):
        self.config = ObjectStorageAPIConfig()
        self.auth_info = self._auth_composite()

        if self.auth_info.auth_strategy == 'saio_tempauth':
            self.storage_url = self.auth_info.access_data.storage_url
            self.auth_token = self.auth_info.access_data.auth_token
        else:
            self.storage_url = self.auth_info.public_url
            self.auth_token = self.auth_info.token_id

        self.client = ObjectStorageAPIClient(
            self.storage_url, self.auth_token)

        self.behaviors = ObjectStorageAPI_Behaviors(
            client=self.client, config=self.config)
