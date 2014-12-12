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

import unittest

from cloudcafe.identity.v3.common.domains.models.responses import Domain


class DomainResponseTests(unittest.TestCase):
    """
    Metatests for v3 Domains response model
    """
    def test_dict_to_obj(self):
        """
        test to verify Domain.dict_to_obj() can convert a dictionary
        representation of a Domain to a Domain object
        """
        # ARRANGE
        domain_dict = {
            'id': 'test_domain_id',
            'name': 'test_domain_name'
        }

        expected_domain_resp_obj = Domain(
            id_='test_domain_id', name='test_domain_name')

        # ACT
        domain_resp_obj = Domain._dict_to_obj(domain_dict)

        # ASSERT
        self.assertEqual(expected_domain_resp_obj, domain_resp_obj)


if __name__ == '__main__':
    unittest.main()
