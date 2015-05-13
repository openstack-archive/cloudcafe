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


import unittest

from cloudcafe.networking.networks.extensions.limits_api.models.response \
    import Limits, Rate, Limit


LIMITS_DATA = (
"""{"limits" : {
    "rate" : [
      {
        "limit" : [
          {
            "unit" : "MINUTE",
            "next-available" : "2015-05-12T21:43:00.182Z",
            "value" : 1000,
            "remaining" : 1000,
            "verb" : "PUT"
          }
        ],
        "uri" : "LoadTestingPUTs",
        "regex" : ".*"
      },
      {
        "limit" : [
          {
            "unit" : "HOUR",
            "next-available" : "2015-05-12T21:43:00.181Z",
            "value" : 1000,
            "remaining" : 1000,
            "verb" : "DELETE"
          },
          {
            "unit" : "HOUR",
            "next-available" : "2015-05-12T21:43:00.181Z",
            "value" : 1000,
            "remaining" : 1000,
            "verb" : "POST"
          },
          {
            "unit" : "HOUR",
            "next-available" : "2015-05-12T21:43:00.181Z",
            "value" : 1000,
            "remaining" : 1000,
            "verb" : "PUT"
          }
        ],
        "uri" : "LoadTestingPorts",
        "regex" : "regex_data"
      }
      ]}}
""")


class GetLimitsTest(unittest.TestCase):
    """Test for the limits (GET) model object response"""
    @classmethod
    def setUpClass(cls):
        """Creating the expected models"""

        limit_obj_a1 = Limit(unit='MINUTE',
                             next_available='2015-05-12T21:43:00.182Z',
                             value=1000, remaining=1000, verb='PUT')
        rate_limits_a = [limit_obj_a1]
        rate_obj_a = Rate(limit=rate_limits_a,
                          uri='LoadTestingPUTs', regex='.*')

        limit_obj_b1 = Limit(unit='HOUR',
                             next_available='2015-05-12T21:43:00.181Z',
                             value=1000, remaining=1000, verb='DELETE')
        limit_obj_b2 = Limit(unit='HOUR',
            next_available='2015-05-12T21:43:00.181Z', value=1000,
            remaining=1000, verb='POST')
        limit_obj_b3 = Limit(unit='HOUR',
                             next_available='2015-05-12T21:43:00.181Z',
                             value=1000, remaining=1000, verb='PUT')
        rate_limits_b = [limit_obj_b1, limit_obj_b2, limit_obj_b3]
        rate_obj_b = Rate(limit=rate_limits_b,
                          uri='LoadTestingPorts', regex='regex_data')
        rate = [rate_obj_a, rate_obj_b]
        cls.expected_response = Limits(rate=rate)

    def test_json_response(self):
        api_json_resp = LIMITS_DATA
        response = Limits()._json_to_obj(api_json_resp)
        msg = ('Unexpected JSON response, expected:\n{0}\n\n'
               'instead of:\n{1}\n').format(self.expected_response,
                                            response)
        self.assertEqual(response, self.expected_response, msg)

if __name__ == "__main__":
    unittest.main()
