from cloudcafe.identity.v3.common.tokens.behavior import TokensBehavior
from cloudcafe.identity.v3.common.tokens.client import TokensClient
from cloudcafe.identity.composites import IdentityBaseComposite


class IdentityV3Composite(IdentityBaseComposite):

    def __init__(self, user_config=None):
        super(IdentityV3Composite, self).__init__(user_config=user_config)
        self.version = 'v3'
        self.tokens_client = TokensClient(
            url=self.url,
            serialize_format=self.ident_config.serialize_format,
            deserialize_format=self.ident_config.deserialize_format,
            auth_token=None)
        self.tokens_behavior = TokensBehavior(self.tokens_client)
        self.load_clients_and_behaviors()

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
