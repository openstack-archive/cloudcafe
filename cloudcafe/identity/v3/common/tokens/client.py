import exceptions

from cloudcafe.identity.common.client import BaseIdentityAPIClient
from cloudcafe.identity.v3.common.tokens.models import responses, request


class ModelNotDefined(exceptions.Exception):
    def __init__(self, model_name):
        self.model_name = model_name

    def __str__(self):
        return "Model name not found: {0}".format(self.model_name)


class TokensClient(BaseIdentityAPIClient):

    def authenticate(self, token_id=None, user_id=None, username=None,
                     password=None, scope=None, user_domain_name=None,
                     user_domain_id=None, domain_name=None, domain_id=None,
                     project_name=None, project_id=None,
                     project_domain_id=None, project_domain_name=None,
                     response_model="default", requestslib_kwargs=None):
        """
        @summary:
        @param token_id: Token to be authenticated
        @type: token_id: String
        @param user_id: User id
        @type: user_id: String
        @param username: Username
        @type: username: String
        @param password: Password
        @type: password: String
        @param scope: Identity the scope to be validated or not
        @type: scope: Boolean
        @param user_domain_name: Domain name of the user
        @type: user_domain_name: String
        @param user_domain_id: Domain id of the user
        @type: user_domain_id: String
        @param domain_name: Domain name of the project
        @type: domain_name: String
        @param domain_id: Domain id of the project
        @type: domain_id: String
        @param project_name: Project name
        @type: project_name: String
        @param project_id: Project id
        @type: project_id: String
        @param project_domain_id: Domain id to be validated with the project
        @type: project_domain_id: String
        @param project_domain_name: Domain name to be validated with project
        @type: project_domain_name: String
        @param requestslib_kwargs: additional kwargs to be sent to requests.
        @type requestslib_kwargs: dictionary
        """

        response_models = {'default': responses.AuthResponse}
        if response_model.lower() not in response_models.keys():
            raise ModelNotDefined(model_name=response_model)
        response_model = response_models[response_model.lower()]

        # POST v3/auth/tokens
        url = "{url}/auth/tokens".format(url=self.url)
        kwargs = {}

        if token_id is not None:
            kwargs["identity"] = request.Identity(
                methods=['token'], token_id=token_id)
        else:
            kwargs["identity"] = request.Identity(
                methods=['password'], user_id=user_id, username=username,
                password=password, user_domain_name=user_domain_name,
                user_domain_id=user_domain_id)

        if scope is not None:
            kwargs["scope"] = request.Scope(
                domain_name=domain_name, domain_id=domain_id,
                project_name=project_name, project_id=project_id,
                project_domain_id=project_domain_id,
                project_domain_name=project_domain_name)

        request_entity = request.Auth(**kwargs)

        return self.post(
            url, response_entity_type=response_model,
            request_entity=request_entity,
            requestslib_kwargs=requestslib_kwargs)

    def validate_token(self, token, nocatalog=None, requestslib_kwargs=None):
        """
        @summary: Validate a token
        @param token: Token to be validated
        @type token: String
        @return: Validate token information
        @rtype: Catalog List
        """

        # GET v3/auth/tokens
        url = "{url}/auth/tokens".format(url=self.url)
        params = {"nocatalog": nocatalog}
        return self.get(url, params=params,
                        headers={'x-subject-token': token},
                        response_entity_type=responses.AuthResponse,
                        requestslib_kwargs=requestslib_kwargs)

    def revoke_token(self, token, requestslib_kwargs=None):
        """
        @summary: Revoke a token
        @param token: Token to be revoked
        @type token: String
        @return: No content
        """

        # DELETE v3/auth/tokens
        url = "{url}/auth/tokens".format(url=self.url)
        return self.delete(url, headers={'x-subject-token': token},
                           requestslib_kwargs=requestslib_kwargs)
