"""
Copyright 2015 Rackspace

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

import time

from cloudcafe.networking.networks.common.behaviors \
    import NetworkingBaseBehaviors, NetworkingResponse
from cloudcafe.networking.networks.common.exceptions \
    import ResourceGetException
from cloudcafe.networking.networks.extensions.limits_api.constants \
    import LimitsResponseCodes


class LimitsBehaviors(NetworkingBaseBehaviors):

    def __init__(self, limits_client, limits_config):
        super(LimitsBehaviors, self).__init__()
        self.config = limits_config
        self.client = limits_client

    def get_limits(self, page_reverse=None,
                   resource_get_attempts=None,
                   raise_exception=False, poll_interval=None):
        """
        @summary: get rate limits
        @param page_reverse: direction of the page
        @type page_reverse: bool
        @param resource_get_attempts: number of API retries
        @type resource_get_attempts: int
        @param raise_exception: flag to raise an exception if the get
            limits call was not as expected or to return None
        @type raise_exception: bool
        @param poll_interval: sleep time interval between API retries
        @type poll_interval: int
        @return: NetworkingResponse object with api response and failure list
        @rtype: common.behaviors.NetworkingResponse
        """
        poll_interval = poll_interval or self.config.api_poll_interval
        resource_get_attempts = (resource_get_attempts or
                                 self.config.api_retries)

        result = NetworkingResponse()
        err_msg = 'Limits GET failure'
        for attempt in range(resource_get_attempts):
            self._log.debug(
                'Attempt {0} of {1} with limits GET'.format(
                    attempt + 1,
                    resource_get_attempts))

            resp = self.client.get_limits(page_reverse=page_reverse)
            resp_check = self.check_response(
                resp=resp,
                status_code=LimitsResponseCodes.GET_LIMITS,
                label='',
                message=err_msg)
            result.response = resp

            # resp_check will have the response failure or None if no failure
            if resp_check is None:
                return result

            # Failures will be an empty list if the list was successful the
            # first time
            result.failures.append(resp_check)
            time.sleep(poll_interval)

        else:
            err_msg = (
                'Unable to GET limits after {0} attempts: '
                '{1}').format(resource_get_attempts, result.failures)
            self._log.error(err_msg)
            if raise_exception:
                raise ResourceGetException(err_msg)
            return result
