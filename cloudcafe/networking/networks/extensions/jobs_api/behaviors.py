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

from cloudcafe.networking.networks.common.behaviors \
    import NetworkingBaseBehaviors
from cloudcafe.networking.networks.extensions.jobs_api.constants \
    import JobsResource, JobsResponseCodes


class JobsBehaviors(NetworkingBaseBehaviors):

    def __init__(self, jobs_client):
        super(JobsBehaviors, self).__init__()
        self.client = jobs_client
        self.response_codes = JobsResponseCodes
        self.jobs_resource = JobsResource(JobsResource.JOB)

    def get_job(self, job_id, resource_get_attempts=None,
                raise_exception=False, poll_interval=None):
        """Get job by ID and verifies response

        Args:
            job_id (str): job ID
            resource_get_attempts (Optional[int]): number of API retries
            raise_exception (Optional[bool]): flag to raise an exception
                if the GET call response is unexpected (default set to False).
            poll_interval (Optional[int]): sleep time interval between API
                retries

        Returns:
            common.behaviors.NetworkingResponse object with API response and
            failure list with failures if any.
        """

        result = self._get_resource(
            resource=self.jobs_resource, resource_id=job_id,
            resource_get_attempts=resource_get_attempts,
            raise_exception=raise_exception, poll_interval=poll_interval)

        return result

    def list_jobs(self, job_id=None, tenant_id=None, transaction_id=None,
                  parent_id=None, subtransactions=None,
                  completed_subtransactions=None, transaction_percent=None,
                  completed=None, action=None, created_at=None, limit=None,
                  marker=None, page_reverse=None,
                  resource_list_attempts=None, raise_exception=False,
                  poll_interval=None):
        """List jobs and verifies the response

        Args:
            job_id (Optional[str]): get job with this ID.
            tenant_id (Optional[str]): get jobs for this tenant ID.
            transaction_id (Optional[str]): get jobs with this transaction ID.
            parent_id (Optional[str]): get jobs with this parent ID.
            subtransactions (Optional[int]): get jobs with this number of
                subtransactions.
            completed_subtransactions (Optional[int]): get jobs with this
                number of completed subtransactions.
            transaction_percent (Optional[int]): get jobs with this completion
                percentage.
            completed (Optional[bool]): get jobs with this true or false flag.
            action (Optional[str]): get jobs with this action,
                for ex. create sg rule <sg_rule_id> or update port <port_id>.
            created_at (Optional[str]): get jobs with this creation date.
            limit (Optional[int]): page size.
            marker (Optional[str]): ID of the last item of the previous page.
            page_reverse (Optional[bool]): direction of the page.
            resource_list_attempts (Optional[int]): number of API retries
            raise_exception (Optional[bool]): flag to raise an exception
                if the GET call response is unexpected (default set to False).
            poll_interval (Optional[int]): sleep time interval between API
                retries

        Returns:
            common.behaviors.NetworkingResponse object with API response and
            failure list with failures if any.
        """
        params_kwargs = dict(
            job_id=job_id, tenant_id=tenant_id, transaction_id=transaction_id,
            parent_id=parent_id, subtransactions=subtransactions,
            completed_subtransactions=completed_subtransactions,
            transaction_percent=transaction_percent, completed=completed,
            action=action, created_at=created_at, limit=limit, marker=marker,
            page_reverse=page_reverse)

        result = self._list_resources(
            resource=self.jobs_resource,
            resource_list_attempts=resource_list_attempts,
            raise_exception=raise_exception, poll_interval=poll_interval,
            params_kwargs=params_kwargs)

        return result
