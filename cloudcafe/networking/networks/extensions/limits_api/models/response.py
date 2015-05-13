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

import json

from cafe.engine.models.base import AutoMarshallingListModel, \
    AutoMarshallingModel


class Limits(AutoMarshallingModel):
    """
    @summary: Limits model response object
    @param rate: rate limit
    @type rate: list
    """

    LIMITS = 'limits'

    def __init__(self, rate=None, **kwargs):
        super(Limits, self).__init__()
        self.rate = rate
        self.kwargs = kwargs

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """Return limits object from a JSON serialized string"""

        limits = None
        json_dict = json.loads(serialized_str)

        json_dict = cls._replace_dict_key(
            json_dict, 'next-available', 'next_available', recursion=True)

        if cls.LIMITS in json_dict:
            limits_dict = json_dict.get(cls.LIMITS)
            limits = Limits(**limits_dict)
            rate = []
            for rate_limit in limits.rate:
                rate_obj = Rate(**rate_limit)
                limit = [Limit(**limit_type) for limit_type in rate_obj.limit]
                rate_obj.limit = limit
                rate.append(rate_obj)
            limits.rate = rate

        return limits


class Rate(AutoMarshallingModel):
    """
    @summary: Rate model response object
    @param limit: rate limit
    @type limit: list
    @param uri: rate limit uniform resource identifyier
    @type uri: str
    @param regex: regular expression for the API URL the rate limit applies
    @type regex: str
    """

    def __init__(self, limit=None, uri=None, regex=None, **kwargs):
        super(Rate, self).__init__()
        self.limit = limit
        self.uri = uri
        self.regex = regex
        self.kwargs = kwargs


class Limit(AutoMarshallingModel):
    """
    @summary: Limit model response object
    @param unit: rate limit time units
    @type unit: str
    @param next_available: datetime when the available rate limits will reset
    @type next_available: str
    @param value: rate limit value
    @type value: int
    @param remaining: remaining rate limits
    @type remaining: int
    @param verb: HTTP request method
    @type verb: str
    """
    def __init__(self, unit=None, next_available=None, value=None,
                 remaining=None, verb=None, **kwargs):
        super(Limit, self).__init__()
        self.unit = unit
        self.next_available = next_available
        self.value = value
        self.remaining = remaining
        self.verb = verb
        self.kwargs = kwargs
