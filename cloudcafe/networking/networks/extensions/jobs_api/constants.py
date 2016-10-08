"""
Copyright 2016 Rackspace

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
from cloudcafe.networking.networks.common.constants \
    import NeutronResource, NeutronResponseCodes, NeutronErrorTypes


class JobsResource(NeutronResource):
    """Jobs resource types"""

    # Resources to be used by the behavior
    JOB = 'job'
    JOBS = 'jobs'

    PLURALS = NeutronResource.PLURALS
    PLURALS.update({JOB: JOBS})


class JobsResponseCodes(NeutronResponseCodes):
    """HTTP Jobs API Response codes"""

    GET_JOB = 200
    LIST_JOBS = 200


class JobsErrorTypes(NeutronErrorTypes):
    """Jobs Error Types"""

    JOB_NOT_FOUND = 'JobNotFound'
