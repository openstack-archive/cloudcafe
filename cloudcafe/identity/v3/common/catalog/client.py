from cloudcafe.identity.common.client import BaseIdentityAPIClient
from cloudcafe.identity.v3.common.catalog.models.response import Catalog


class CatalogClient(BaseIdentityAPIClient):

    def get_catalog(self, requestslib_kwargs=None):
        """
        @summary: Fetching a service catalog
        @return: Catalog information
        @rtype: Catalog List
        """

        # GET v3/auth/catalog
        url = "{url}/auth/catalog".format(url=self.url)
        return self.get(url, response_entity_type=Catalog,
                        requestslib_kwargs=requestslib_kwargs)
