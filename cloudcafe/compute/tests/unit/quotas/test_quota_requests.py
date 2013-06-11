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

import unittest2 as unittest

from cloudcafe.compute.quotas_api.models.requests import UpdateQuotaRequest


class QuotaRequestsTest(unittest.TestCase):

    def test_serialize_host_update_request_to_json(self):
        quota_obj = UpdateQuotaRequest(security_groups=45)
        json_serialized_quota = quota_obj.serialize("json")
        expected_json = '{"quota_set": {"security_group_rules": 45}}'
        self.assertEqual(json_serialized_quota, expected_json)

    def test_serialize_host_update_request_to_xml(self):
        quota_obj = UpdateQuotaRequest(security_groups=45, id='fake_tenant')
        xml_serialized_quota = quota_obj.serialize("xml")
        expected_xml = '<?xml version=\'1.0\' encoding=\'UTF-8\'?>' \
                       '<quota_set id="fake_tenant">' \
                       '<security_group_rules>45</security_group_rules>' \
                       '</quota_set>'
        self.assertEqual(xml_serialized_quota, expected_xml)

if __name__ == '__main__':
    unittest.main()
