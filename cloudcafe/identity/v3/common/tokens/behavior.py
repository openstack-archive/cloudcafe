from cafe.engine.behaviors import BaseBehavior


class TokensBehavior(BaseBehavior):

    def __init__(self, client):
        super(TokensBehavior, self).__init__()
        self.client = client

    def authenticate(self, username, password):
        """
        @summary Authenticate the user with username and password
        """

        if self.client.url.endswith("v3") or self.client.url.endswith("v3/"):
            pass
        else:
            self.client.url = '{0}/v3'.format(self.client.url)

        auth_response = self.client.authenticate(
            username=username, password=password)
        if not auth_response.ok:
            raise Exception("Failed to authenticate")
        if auth_response.entity is None:
            raise Exception("Failed to parse Auth response Body")
        return auth_response
