"""
Copyright 2013 Rackspace

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

from cafe.engine.behaviors import BaseBehavior


class BaseComputeBehavior(BaseBehavior):

    def verify_entity(self, response):
        """Verifies if a request was successful and if an entity was
        properly deserialized."""
        if not response.ok:
            msg = "Call failed with status_code {0} ".format(
                response.status_code)
            self._log.error(msg)
            raise Exception(msg)

        if response.entity is None:
            msg = "Response body did not deserialize as expected"
            self._log.error(msg)
            raise Exception(msg)

        return response.entity