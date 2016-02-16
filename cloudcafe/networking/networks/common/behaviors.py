"""
Copyright 2014 Rackspace

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import requests
import time

from cafe.engine.behaviors import BaseBehavior
from cloudcafe.common.tools.datagen import rand_name
from cloudcafe.networking.networks.common.config import NetworkingBaseConfig
from cloudcafe.networking.networks.common.constants \
    import NeutronResponseCodes, NeutronResource
from cloudcafe.networking.networks.common.exceptions \
    import ResourceBuildException, ResourceDeleteException, \
    ResourceGetException, ResourceListException, ResourceUpdateException, \
    UnhandledMethodCaseException


class NetworkingBaseBehaviors(BaseBehavior):
    """Behaviors parent class

    To be inherited by all networks api behaviors and can be called for ex.

    net = NetworkingComposite()
    net.common.behaviors.wait_for_status(port, 'ACTIVE')

    or
    net.ports.behaviors.wait_for_status_status(port, 'ACTIVE')

    in this last call methods and config values will be overwritten if present
    in the ports config
    """

    def __init__(self):
        super(NetworkingBaseBehaviors, self).__init__()
        self.config = NetworkingBaseConfig()

    def check_response(self, resp, status_code, label, message,
                       network_id=None):
        """
        @summary: Checks the API response object
        @param resp: API call response object
        @type resp: requests.models.Response
        @param status_code: HTTP expected response code
        @type status_code: int
        @param label: resource identifier like name, label, ID, etc.
        @type label: string
        @param message: error message like Network Get failure for ex.
        @type message: string
        @param network_id: related Network ID (optional)
        @type network_id: string
        @return: None if the response is the expected or the error message
        @rtype: None or string
        """
        response_msg = None
        if network_id:
            label = '{label} at network {network}'.format(
                label=label, network=network_id)

        resp_type = type(resp)
        if not resp_type == requests.models.Response:
            err_msg = ('{label} {message}: Unexpected response object '
                       'type {resp_type}').format(label=label, message=message,
                                                  resp_type=resp_type)
            self._log.error(err_msg)
            response_msg = err_msg

        elif resp.ok and resp.entity and resp.status_code == status_code:
            response_msg = None

        elif not resp.ok or resp.status_code != status_code:
            err_msg = (
                '{label} {message}: {status} {reason} '
                '{content}. Expected status code {expected_status}').format(
                    label=label, message=message, status=resp.status_code,
                    reason=resp.reason, content=resp.content,
                    expected_status=status_code)
            self._log.error(err_msg)
            response_msg = err_msg
        elif not resp.entity:
            err_msg = ('{label} {message}: Unable to get response'
                       ' entity object').format(label=label, message=message)
            self._log.error(err_msg)
            response_msg = err_msg
        else:

            # This should NOT happen, scenarios should be covered by the elifs
            err_msg = 'Unhandled check response base behavior case'
            raise UnhandledMethodCaseException(err_msg)
        return response_msg

    def filter_entity_list_by_name(self, entity_list, name):
        """
        @summary: Filters an entity list by name
        @param entity_list: List of instances with the name attribute
        @type entity_list: list(instances)
        @param name: name or name_starts_with* to filter by
        @type name: str
        @return: filtered entity list by name
        @rtype: list(instances)
        """
        new_entity_list = []
        starts_with_name = False
        name = name.strip()
        if name[-1] == '*':
            name = name[:-1]
            starts_with_name = True
        for entity in entity_list:
            if entity.name == name:
                new_entity_list.append(entity)
            elif starts_with_name and entity.name.startswith(name):
                new_entity_list.append(entity)
        return new_entity_list

    def filter_entity_list_by_attr(self, entity_list, attr, value):
        """
        @summary: Filters an entity list by attribute
        @param entity_list: List of instances
        @type entity_list: list(instances)
        @param attr: entity attribute to filter by
        @type attr: str
        @param value: entity attribute value to filter by
        @type value: str
        @return: filtered entity list by attribute
        @rtype: list(instances)
        """
        new_entity_list = []
        for entity in entity_list:
            if hasattr(entity, attr):
                attr_value = getattr(entity, attr)
                if attr_value == value:
                    new_entity_list.append(entity)
        return new_entity_list

    def get_id_list_from_entity_list(self, entity_list, name=None):
        """
        @summary: Gets an id list from an entity list
        @param entity_list: List of instances with the name and id attributes
        @type entity_list: list(instances)
        @param name: (optional) name or name_starts_with* to filter by
        @type name: str
        @return: ID list
        @rtype: list
        """
        if name:
            entity_list = self.filter_entity_list_by_name(entity_list, name)
        id_list = [entity.id for entity in entity_list]
        return id_list

    def __over_limit_retry(self, resource_type, timeout, poll_interval,
                           status_code, resp, fn_name, fn_kwargs):
        """
        @summary: Retry mechanism for API rate limited calls
        @param resource_type: type of resource for ex. networks, subnets, etc.
            See NeutronResourceTypes in the networks constants
        @type resource_type: str
        @param timeout: timeout for over limit retries
        @type timeout: int
        @param poll_interval: sleep time interval between API retries
        @type poll_interval: int
        @param status_code: over limit API HTTP response code
        @type: int
        @param resp: API call response object
        @type resp: Requests.response
        @param fn_name: API function name
        @type fn_name: str
        @param fn_kwargs: API function arguments
        @type fn_kwargs: dict
        """
        endtime = time.time() + int(timeout)
        retry_msg = ('OverLimit retry with a {timeout}s timeout '
                     'calling {resource_type} function {fn_name}').format(
                         timeout=timeout, resource_type=resource_type,
                         fn_name=fn_name)
        self._log.info(retry_msg)
        while (resp.status_code == status_code and
               time.time() < endtime):
            resp = getattr(self.client, fn_name)(**fn_kwargs)
            time.sleep(poll_interval)
        return resp

    def _create_resource(self, resource, resource_build_attempts=None,
                         raise_exception=True, poll_interval=None,
                         has_name=True, use_exact_name=False,
                         attrs_kwargs=None, timeout=None,
                         use_over_limit_retry=False):
        """
        @summary: Creates and verifies a resource is created as expected
        @param resource: type of resource for ex. network, subnet, port, etc.
            See NeutronResource in the networks constants
        @type resource: resource instance with singular and plural forms
        @param resource_build_attempts: number of API retries
        @type resource_build_attempts: int
        @param raise_exception: flag to raise an exception if the
            resource was not created or to return None
        @type raise_exception: bool
        @param poll_interval: sleep time interval between API retries
        @type poll_interval: int
        @param has_name: if the resource has a name attribute
        @type has_name: bool
        @param use_exact_name: flag if the exact name given should be used
        @type use_exact_name: bool
        @param attrs_kwargs: resource attributes to create with, for ex. name
        @type attrs_kwargs: dict
        @param timeout: resource create timeout for over limit retries
        @type timeout: int
        @param use_over_limit_retry: flag to enable/disable the create
            over limits retries
        @type use_over_limit_retry: bool
        @return: NetworkingResponse object with api response and failure list
        @rtype: common.behaviors.NetworkingResponse
        """

        # Defining the resource type in singular form (for ex. network)
        resource_type = resource.singular

        # If has_name is False name can be used as a reference for log messages
        name = attrs_kwargs.get('name')
        if has_name:
            if name is None:
                name = rand_name(self.config.starts_with_name)
            elif not use_exact_name:
                name = rand_name(name)
            attrs_kwargs['name'] = name
        else:
            # In case name is NOT used as a reference for log messages
            if name is None:
                name = ''

        poll_interval = poll_interval or self.config.api_poll_interval
        resource_build_attempts = (resource_build_attempts or
                                   self.config.api_retries)
        use_over_limit_retry = (use_over_limit_retry or
                                self.config.use_over_limit_retry)
        timeout = timeout or self.config.resource_create_timeout

        result = NetworkingResponse()
        err_msg = '{0} Create failure'.format(resource_type)
        for attempt in range(resource_build_attempts):
            self._log.debug(
                'Attempt {attempt_n} of {attempts} creating '
                '{resource_type}'.format(
                    attempt_n=attempt + 1,
                    attempts=resource_build_attempts,
                    resource_type=resource_type))

            # Method uses resource type in singular form (slicing the ending s)
            create_fn_name = 'create_{0}'.format(resource_type)
            resp = getattr(self.client, create_fn_name)(**attrs_kwargs)

            if use_over_limit_retry:
                entity_too_large_status_code = (getattr(self.response_codes,
                                                'REQUEST_ENTITY_TOO_LARGE'))
                if resp.status_code == entity_too_large_status_code:
                    fn_kwargs = attrs_kwargs

                    resp = self.__over_limit_retry(
                        resource_type=resource_type, timeout=timeout,
                        poll_interval=poll_interval,
                        status_code=entity_too_large_status_code,
                        resp=resp, fn_name=create_fn_name,
                        fn_kwargs=fn_kwargs)

            response_code = create_fn_name.upper()
            status_code = getattr(self.response_codes, response_code)
            resp_check = self.check_response(
                resp=resp, status_code=status_code, label=name,
                message=err_msg)

            result.response = resp
            if not resp_check:
                return result

            # Failures will be an empty list if the create was successful the
            # first time
            result.failures.append(resp_check)
            time.sleep(poll_interval)

        else:
            err_msg = (
                'Unable to CREATE {name} {resource_type} after '
                '{attempts} attempts: {failures}').format(
                    name=name, resource_type=resource_type,
                    attempts=resource_build_attempts,
                    failures=result.failures)
            self._log.error(err_msg)
            if raise_exception:
                raise ResourceBuildException(err_msg)
            return result

    def _update_resource(self, resource, resource_id,
                         resource_update_attempts=None, raise_exception=False,
                         poll_interval=None, attrs_kwargs=None,
                         timeout=None, use_over_limit_retry=False):
        """
        @summary: Updates and verifies a specified resource
        @param resource: type of resource for ex. network, subnet, port, etc.
            See NeutronResource in the networks constants
        @type resource: resource instance with singular and plural forms
        @param resource_id: The UUID for the resource
        @type resource_id: str
        @param resource_update_attempts: number of API retries
        @type resource_update_attempts: int
        @param raise_exception: flag to raise an exception if the
            resource was not updated or to return None
        @type raise_exception: bool
        @param poll_interval: sleep time interval between API retries
        @type poll_interval: int
        @param attrs_kwargs: resource attributes to update
        @type attrs_kwargs: dict
        @param timeout: resource update timeout for over limit retries
        @type timeout: int
        @param use_over_limit_retry: flag to enable/disable the update
            over limits retries
        @type use_over_limit_retry: bool
        @return: NetworkingResponse object with api response and failure list
        @rtype: common.behaviors.NetworkingResponse
        """

        # Defining the resource type in singular form (for ex. network)
        resource_type = resource.singular

        poll_interval = poll_interval or self.config.api_poll_interval
        resource_update_attempts = (resource_update_attempts or
                                    self.config.api_retries)
        use_over_limit_retry = (use_over_limit_retry or
                                self.config.use_over_limit_retry)
        timeout = timeout or self.config.resource_update_timeout

        result = NetworkingResponse()
        err_msg = '{0} Update failure'.format(resource_type)
        for attempt in range(resource_update_attempts):
            self._log.debug(
                'Attempt {attempt_n} of {attempts} updating {resource_type} '
                '{resource_id}'.format(attempt_n=attempt + 1,
                                       attempts=resource_update_attempts,
                                       resource_type=resource_type,
                                       resource_id=resource_id))

            # Method uses resource type in singular form (slicing the ending s)
            update_fn_name = 'update_{0}'.format(resource_type)

            # Resource ID is expected to be the first client method parameter
            resp = getattr(self.client, update_fn_name)(resource_id,
                                                        **attrs_kwargs)

            if use_over_limit_retry:
                entity_too_large_status_code = (getattr(self.response_codes,
                                                'REQUEST_ENTITY_TOO_LARGE'))
                if resp.status_code == entity_too_large_status_code:
                    fn_kwargs = attrs_kwargs

                    # Adding the resource id to the function kwargs
                    resource_id_name = '{0}_id'.format(resource_type)
                    fn_kwargs[resource_id_name] = resource_id

                    resp = self.__over_limit_retry(
                        resource_type=resource_type, timeout=timeout,
                        poll_interval=poll_interval,
                        status_code=entity_too_large_status_code,
                        resp=resp, fn_name=update_fn_name,
                        fn_kwargs=fn_kwargs)

            response_code = update_fn_name.upper()
            status_code = getattr(self.response_codes, response_code)
            resp_check = self.check_response(
                resp=resp, status_code=status_code, label=resource_id,
                message=err_msg)

            result.response = resp
            if not resp_check:
                return result

            # Failures will be an empty list if the update was successful the
            # first time
            result.failures.append(resp_check)
            time.sleep(poll_interval)

        else:
            err_msg = (
                'Unable to UPDATE {resource_id} {resource_type} after '
                '{attempts} attempts: {failures}').format(
                    resource_id=resource_id, resource_type=resource_type,
                    attempts=resource_update_attempts,
                    failures=result.failures)
            self._log.error(err_msg)
            if raise_exception:
                raise ResourceUpdateException(err_msg)
            return result

    def _get_resource(self, resource, resource_id, resource_get_attempts=None,
                      raise_exception=False, poll_interval=None, timeout=None,
                      use_over_limit_retry=False, fn_kwargs=None):
        """
        @summary: Shows and verifies a specified resource
        @param resource: type of resource for ex. network, subnet, port, etc.
            See NeutronResource in the networks constants
        @type resource: resource instance with singular and plural forms
        @param resource_id: The UUID for the resource
        @type resource_id: str
        @param fn_kwargs: function client call params besides the ID
        @type fn_kwargs: dict
        @param resource_get_attempts: number of API retries
        @type resource_get_attempts: int
        @param raise_exception: flag to raise an exception if the get
            resource was not as expected or to return None
        @type raise_exception: bool
        @param poll_interval: sleep time interval between API retries
        @type poll_interval: int
        @param timeout: resource get timeout for over limit retries
        @type timeout: int
        @param use_over_limit_retry: flag to enable/disable the get
            over limits retries
        @type use_over_limit_retry: bool
        @return: NetworkingResponse object with api response and failure list
        @rtype: common.behaviors.NetworkingResponse
        """

        # Defining the resource type in singular form (for ex. network)
        resource_type = resource.singular

        poll_interval = poll_interval or self.config.api_poll_interval
        resource_get_attempts = (resource_get_attempts or
                                 self.config.api_retries)
        use_over_limit_retry = (use_over_limit_retry or
                                self.config.use_over_limit_retry)
        timeout = timeout or self.config.resource_get_timeout

        result = NetworkingResponse()
        err_msg = '{0} Get failure'.format(resource_type)
        for attempt in range(resource_get_attempts):
            self._log.debug(
                'Attempt {attempt_n} of {attempts} getting {resource_type} '
                '{resource_id}'.format(attempt_n=attempt + 1,
                                       attempts=resource_get_attempts,
                                       resource_type=resource_type,
                                       resource_id=resource_id))

            fn_kwargs = fn_kwargs or {}

            # Adding the resource id to the function kwargs
            resource_id_name = '{0}_id'.format(resource_type)
            fn_kwargs[resource_id_name] = resource_id

            # Method uses resource type in singular form (slicing the ending s)
            get_fn_name = 'get_{0}'.format(resource_type)
            resp = getattr(self.client, get_fn_name)(**fn_kwargs)

            if use_over_limit_retry:
                entity_too_large_status_code = (getattr(self.response_codes,
                                                'REQUEST_ENTITY_TOO_LARGE'))
                if resp.status_code == entity_too_large_status_code:
                    resp = self.__over_limit_retry(
                        resource_type=resource_type, timeout=timeout,
                        poll_interval=poll_interval,
                        status_code=entity_too_large_status_code,
                        resp=resp, fn_name=get_fn_name,
                        fn_kwargs=fn_kwargs)

            response_code = get_fn_name.upper()
            status_code = getattr(self.response_codes, response_code)
            resp_check = self.check_response(
                resp=resp,
                status_code=status_code,
                label=resource_id,
                message=err_msg)

            result.response = resp
            if not resp_check:
                return result

            # Failures will be an empty list if the get was successful the
            # first time
            result.failures.append(resp_check)
            time.sleep(poll_interval)

        else:
            err_msg = (
                'Unable to GET {resource_id} {resource_type} after {attempts} '
                'attempts: {failures}').format(resource_id=resource_id,
                                               resource_type=resource_type,
                                               attempts=resource_get_attempts,
                                               failures=result.failures)
            self._log.error(err_msg)
            if raise_exception:
                raise ResourceGetException(err_msg)
            return result

    def _list_resources(self, resource, resource_list_attempts=None,
                        raise_exception=False, poll_interval=None,
                        params_kwargs=None, timeout=None,
                        use_over_limit_retry=False):
        """
        @summary: Lists resources and verifies the response is the expected
        @param resource: type of resource for ex. network, subnet, port, etc.
            See NeutronResource in the networks constants
        @type resource: resource instance with singular and plural forms
        @param resource_list_attempts: number of API retries
        @type resource_list_attempts: int
        @param raise_exception: flag to raise an exception if the resource list
            was not as expected or to return None
        @type raise_exception: bool
        @param poll_interval: sleep time interval between API retries
        @type poll_interval: int
        @param params_kwargs: key value params to filter by the list results
        @type params_kwargs: dict
        @param timeout: resource list timeout for over limit retries
        @type timeout: int
        @param use_over_limit_retry: flag to enable/disable the list
            over limits retries
        @type use_over_limit_retry: bool
        @return: NetworkingResponse object with api response and failure list
        @rtype: common.behaviors.NetworkingResponse
        """

        # Defining the resource type in plural form (for ex. networks)
        resource_type = resource.plural

        poll_interval = poll_interval or self.config.api_poll_interval
        resource_list_attempts = (resource_list_attempts or
                                  self.config.api_retries)
        use_over_limit_retry = (use_over_limit_retry or
                                self.config.use_over_limit_retry)
        timeout = timeout or self.config.resource_get_timeout

        result = NetworkingResponse()
        err_msg = '{0} list failure'.format(resource_type)
        for attempt in range(resource_list_attempts):
            self._log.debug(
                'Attempt {attempt_n} of {attempts} with {resource_type} '
                'list'.format(attempt_n=attempt + 1,
                              attempts=resource_list_attempts,
                              resource_type=resource_type))

            list_fn_name = 'list_{0}'.format(resource_type)
            resp = getattr(self.client, list_fn_name)(**params_kwargs)

            if use_over_limit_retry:
                entity_too_large_status_code = (getattr(self.response_codes,
                                                'REQUEST_ENTITY_TOO_LARGE'))
                if resp.status_code == entity_too_large_status_code:
                    fn_kwargs = params_kwargs

                    resp = self.__over_limit_retry(
                        resource_type=resource_type, timeout=timeout,
                        poll_interval=poll_interval,
                        status_code=entity_too_large_status_code,
                        resp=resp, fn_name=list_fn_name,
                        fn_kwargs=fn_kwargs)

            response_code = list_fn_name.upper()
            status_code = getattr(self.response_codes, response_code)
            resp_check = self.check_response(
                resp=resp, status_code=status_code, label='', message=err_msg)

            result.response = resp
            if not resp_check:
                return result

            # Failures will be an empty list if the list was successful the
            # first time
            result.failures.append(resp_check)
            time.sleep(poll_interval)

        else:
            err_msg = (
                'Unable to LIST {resource_type} after {attempts} attempts: '
                '{failures}').format(resource_type=resource_type,
                                     attempts=resource_list_attempts,
                                     failures=result.failures)
            self._log.error(err_msg)
            if raise_exception:
                raise ResourceListException(err_msg)
            return result

    def _delete_resource(self, resource, resource_id,
                         resource_delete_attempts=None, raise_exception=False,
                         poll_interval=None, timeout=None,
                         use_over_limit_retry=False):
        """
        @summary: Deletes and verifies a specified resource is deleted
        @param resource: type of resource for ex. network, subnet, port, etc.
            See NeutronResource in the networks constants
        @type resource: resource instance with singular and plural forms
        @param resource_id: The UUID for the resource
        @type resource_id: string
        @param resource_delete_attempts: number of API retries
        @type resource_delete_attempts: int
        @param raise_exception: flag to raise an exception if the deleted
            resource was not as expected or to return None
        @type raise_exception: bool
        @param poll_interval: sleep time interval between API retries
        @type poll_interval: int
        @param timeout: resource delete timeout for over limit retries
        @type timeout: int
        @param use_over_limit_retry: flag to enable/disable the delete
            over limits retries
        @type use_over_limit_retry: bool
        @return: NetworkingResponse object with api response and failure list
        @rtype: common.behaviors.NetworkingResponse
        """

        # Defining the resource type in singular form (for ex. network)
        resource_type = resource.singular

        poll_interval = poll_interval or self.config.api_poll_interval
        resource_delete_attempts = (resource_delete_attempts or
                                    self.config.api_retries)
        use_over_limit_retry = (use_over_limit_retry or
                                self.config.use_over_limit_retry)
        timeout = timeout or self.config.resource_get_timeout

        result = NetworkingResponse()
        for attempt in range(resource_delete_attempts):
            self._log.debug(
                'Attempt {attempt_n} of {attempts} deleting {resource_type} '
                '{resource_id}'.format(attempt_n=attempt + 1,
                                       attempts=resource_delete_attempts,
                                       resource_type=resource_type,
                                       resource_id=resource_id))

            # Method uses resource type in singular form (slicing the ending s)
            delete_fn_name = 'delete_{0}'.format(resource_type)
            resp = getattr(self.client, delete_fn_name)(resource_id)

            if use_over_limit_retry:
                entity_too_large_status_code = (getattr(self.response_codes,
                                                'REQUEST_ENTITY_TOO_LARGE'))
                if resp.status_code == entity_too_large_status_code:
                    fn_kwargs = {}

                    # Adding the resource id to the function kwargs
                    resource_id_name = '{0}_id'.format(resource_type)
                    fn_kwargs[resource_id_name] = resource_id

                    resp = self.__over_limit_retry(
                        resource_type=resource_type, timeout=timeout,
                        poll_interval=poll_interval,
                        status_code=entity_too_large_status_code,
                        resp=resp, fn_name=delete_fn_name,
                        fn_kwargs=fn_kwargs)

            result.response = resp

            # Delete response is without entity so resp_check can not be used
            response_code = delete_fn_name.upper()
            status_code = getattr(self.response_codes, response_code)
            if resp.ok and resp.status_code == status_code:
                return result

            err_msg = ('{resource_id} {resource_type} Delete failure, expected'
                       'status code: {expected_status}. Response: {status} '
                       '{reason} {content}').format(
                           resource_id=resource_id,
                           resource_type=resource_type,
                           expected_status=status_code,
                           status=resp.status_code,
                           reason=resp.reason,
                           content=resp.content)
            self._log.error(err_msg)
            result.failures.append(err_msg)
            time.sleep(poll_interval)

        else:
            err_msg = (
                'Unable to DELETE {resource_id} {resource_type} after '
                '{attempts} attempts: {failures}').format(
                    resource_id=resource_id, resource_type=resource_type,
                    attempts=resource_delete_attempts,
                    failures=result.failures)
            self._log.error(err_msg)
            if raise_exception:
                raise ResourceDeleteException(err_msg)
            return result

    def _delete_resources(self, resource, resource_list=None, name=None,
                          tenant_id=None, skip_delete=None):
        """
        @summary: deletes multiple resources (for ex. networks)
        @param resource: type of resource for ex. network, subnet, port, etc.
            See NeutronResource in the networks constants
        @type resource: resource instance with singular and plural forms
        @param resource_list: list of resource UUIDs
        @type resource_list: list(str)
        @param name: resource name to filter by, asterisk can be used at the
            end of the name to filter by name starts with, for ex. name*
            (name will be ignored if resource_list given)
        @type name: string
        @param tenant_id: resource tenant ID to filter by
        @type tenant_id: string (ignored if resource_list given)
        @param skip_delete: list of resource UUIDs that should skip deletion
        @type skip_delete: list
        @return: failed delete list with resource UUIDs and failures
        @rtype: list(dict)
        """

        # Defining the resource type in singular and plural forms
        resource_type_singular = resource.singular
        resource_type_plural = resource.plural

        # Getting the resource list based on the resource type (if not given)
        if resource_list is None:
            list_fn_name = 'list_{0}'.format(resource_type_plural)
            resp = getattr(self, list_fn_name)(tenant_id=tenant_id)

            # Getting the Neutron expected response based on the fn name
            response_code = list_fn_name.upper()
            status_code = getattr(self.response_codes, response_code)

            if resp.response.status_code != status_code:
                get_msg = 'Unable to get {0} for delete_{0} call'.format(
                    resource_type_plural)
                self._log.info(get_msg)
                return None
            resources = resp.response.entity

            # In case the filtering on the GET call did NOT work as expected
            if tenant_id:
                resources = self.filter_entity_list_by_attr(
                    entity_list=resources, attr='tenant_id', value=tenant_id)

            resource_list = self.get_id_list_from_entity_list(
                entity_list=resources, name=name)

        # Getting resources that should Not be deleted
        do_not_delete = []
        false_values = [None, '']
        if skip_delete is not None:
            do_not_delete.extend(skip_delete)

        if resource_type_plural == NeutronResource.NETWORKS:
            property_list = ['public_network_id', 'service_network_id']
            for prop in property_list:
                if (hasattr(self.config, prop) and
                        getattr(self.config, prop) not in false_values):
                    do_not_delete.append(getattr(self.config, prop))

        # Removing the resources that should NOT be deleted if any
        for resource_to_skip in do_not_delete:
            if resource_to_skip in resource_list:
                resource_list.remove(resource_to_skip)

        log_msg = 'Deleting {0}: {1}'.format(resource_type_plural,
                                             resource_list)
        self._log.info(log_msg)
        failed_deletes = []
        delete_fn_name = 'delete_{0}'.format(resource_type_singular)
        for resource_id in resource_list:
            result = getattr(self, delete_fn_name)(resource_id)
            if result.failures:
                failed_deletes.append(result.failures)
        return failed_deletes

    def _clean_resource(self, resource, resource_id, timeout=None,
                        poll_interval=None):
        """
        @summary: deletes a resource within a time out
        @param resource: type of resource for ex. network, subnet, port, etc.
            See NeutronResource in the networks constants
        @type resource: resource instance with singular and plural forms
        @param resource_id: The UUID for the for the resource
        @type resource_id: str
        @param timeout: seconds to wait for the resource to be deleted
        @type timeout: int
        @param poll_interval: sleep time interval between API delete/get calls
        @type poll_interval: int
        @return: None if delete was successful or the undeleted resource_id
        @rtype: None or string
        """

        # Defining the resource type in singular form (for ex. network)
        resource_type = resource.singular

        timeout = timeout or self.config.resource_delete_timeout
        poll_interval = poll_interval or self.config.api_poll_interval
        endtime = time.time() + int(timeout)
        log_msg = ('Deleting {resource_id} {resource_type} within a {timeout}s'
                   ' timeout').format(resource_id=resource_id,
                                      resource_type=resource_type,
                                      timeout=timeout)
        self._log.info(log_msg)

        # Method uses resource type in singular form (slicing the ending s)
        delete_fn_name = 'delete_{0}'.format(resource_type)
        get_fn_name = 'get_{0}'.format(resource_type)
        resp = None
        while time.time() < endtime:
            try:
                getattr(self.client, delete_fn_name)(resource_id)
                resp = getattr(self.client, get_fn_name)(resource_id)
            except Exception as err:
                err_msg = ('Encountered an exception deleting a '
                           '{resource_type} within the _clean_resource method.'
                           ' Exception: {error}').format(
                               resource_type=resource_type, error=err)
                self._log.error(err_msg)

            if (resp is not None and
                    resp.status_code == NeutronResponseCodes.NOT_FOUND):
                return None
            time.sleep(poll_interval)

        err_msg = (
            'Unable to delete {resource_id} {resource_type} within a '
            '{timeout}s timeout').format(resource_id=resource_id,
                                         resource_type=resource_type,
                                         timeout=timeout)
        self._log.error(err_msg)
        return resource_id

    def _clean_resources(self, resource, resource_list, timeout=None,
                         poll_interval=None):
        """
        @summary: deletes each resource from a list calling _clean_resource
        @param resource: type of resource for ex. network, subnet, port, etc.
            See NeutronResource in the networks constants
        @type resource: resource instance with singular and plural forms
        @param resource_list: list of resource UUIDs to delete
        @type resource_list: list(str)
        @param timeout: seconds to wait for the resource to be deleted
        @type timeout: int
        @param poll_interval: sleep time interval between API delete/get calls
        @type poll_interval: int
        @return: list of undeleted resource UUIDs
        @rtype: list(str)
        """

        # Defining the resource type in plural form (for ex. networks)
        resource_type_plural = resource.plural

        log_msg = 'Deleting {resource_type}: {resource_list}'.format(
            resource_type=resource_type_plural, resource_list=resource_list)
        self._log.info(log_msg)
        undeleted_resources = []
        for resource_id in resource_list:

            # _cleanup_resource takes the resource obj
            result = self._clean_resource(resource=resource,
                                          resource_id=resource_id,
                                          timeout=timeout,
                                          poll_interval=poll_interval)
            if result:
                undeleted_resources.append(result)
        if undeleted_resources:
            err_msg = (
                'Unable to delete {resource_type}: '
                '{undeleted_resources}').format(
                    resource_type=resource_type_plural,
                    undeleted_resources=undeleted_resources)
            self._log.error(err_msg)
        return undeleted_resources


class NetworkingResponse(object):
    """
    @summary:
    @param response: response object for client calls done by behavior methods,
        can also be set to None (for ex. there was no entity obj.),
        True (for ex. the delete was successful) or False
    @type response: Requests.response, None or bool
    @param failures: list with error messages created by the check_response
        method. Empty list if no errors were found while checking the response
    @type failures: list
    """
    def __init__(self):
        self.response = None
        self.failures = list()

    def __repr__(self):
        return 'response: {0}\nfailures: {1}'.format(self.response,
                                                     self.failures)
