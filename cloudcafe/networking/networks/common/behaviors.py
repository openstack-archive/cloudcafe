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
from cloudcafe.networking.networks.common.config import NetworkingBaseConfig
from cloudcafe.networking.networks.common.exceptions \
    import UnhandledMethodCaseException


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
            err_msg = ('{label} {message}: {status} {reason} '
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
