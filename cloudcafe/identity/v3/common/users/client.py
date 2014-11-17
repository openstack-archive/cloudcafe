from cloudcafe.identity.common.client import BaseIdentityAPIClient
from cloudcafe.identity.v3.common.users.models import response


class UsersClient(BaseIdentityAPIClient):

    def list_users(self, requestslib_kwargs=None):
        """
        @summary: Fetching the users
        @return: User information
        @rtype: User List
        """
        url = "{0}/users".format(self.url)
        return self.get(
            url, response_entity_type=response.User,
            requestslib_kwargs=requestslib_kwargs)
