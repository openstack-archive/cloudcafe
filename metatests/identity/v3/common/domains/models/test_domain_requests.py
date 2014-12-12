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

from cloudcafe.identity.v3.common.domains.models.requests import Domain


class DomainRequestsTests(unittest.TestCase):
    """
    Metatests for v3 Domain request model
    """
    def test_obj_to_dict(self):
        """
        test to verify Domain.obj_to_dict() can convert a Domain object to
        a dictionary
        """
        # ARRANGE
        test_domain_obj = Domain(name='test_domain', id_='test_id')

        expected_domain_dict = {
            'name': 'test_domain',
            'id': 'test_id'
        }
        # ACT
        test_domain_dict = test_domain_obj._obj_to_dict()
        # ASSERT
        self.assertEqual(expected_domain_dict, test_domain_dict)


if __name__ == '__main__':
    unittest.main()
