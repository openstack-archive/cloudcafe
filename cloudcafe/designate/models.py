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

from cafe.engine.models.base import AutoMarshallingModel


class Links(AutoMarshallingModel):
    """Represents the links section of a paginated response in the v2 API."""

    def __init__(self, link_self=None, link_next=None):
        self.link_self = link_self
        self.link_next = link_next

    @classmethod
    def _from_dict(cls, links_dict):
        return Links(link_self = links_dict.get("self"),
                     link_next = links_dict.get("next"))
