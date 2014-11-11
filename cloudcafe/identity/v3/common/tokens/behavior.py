from cafe.engine.behaviors import BaseBehavior


class TokensBehaviorException(Exception):
    pass


class TokensBehavior(BaseBehavior):

    def __init__(self, client):
        super(TokensBehavior, self).__init__()
        self.client = client

    def authenticate(self, username, password):
        """
        @summary Authenticate the user with username and password
        """

        if not self.client.url.endswith(("v3", "v3/")):
            self.client.url = '{url}/v3'.format(url=self.client.url)

        auth_response = self.client.authenticate(
            username=username, password=password)
        self._verify_entity(auth_response)
        return auth_response

    def _verify_entity(self, resp):
        """
        Verify authentication call succeeded and verify auth response entity
        deserialized correctly
        """
        if not resp.ok:
            msg = "Auth failed with status_code {0} ".format(resp.status_code)
            self._log.error(msg)
            raise TokensBehaviorException(msg)

        if resp.entity is None:
            msg = "Response body did not deserialize as expected"
            self._log.error(msg)
            raise TokensBehaviorException(msg)
        return resp.entity
