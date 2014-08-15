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

import copy
import json
import xml.etree.ElementTree as ET

from cloudcafe.networking.common.models.port import Port


class PortResponse(Port):
    """Port response model"""

    def _json_to_obj(self, serialized_str):
        """Return port object from a JSON serialized string"""

        ret = None
        json_response = json.loads(serialized_str)

        # Creating a deep copy just in case later we want the original resp
        json_dict = copy.deepcopy(json_response)

        # Replacing attribute response names if they are Python reserved words
        # with a trailing underscore, for ex. id for id_ or if they have a
        # special character within the name replacing it for an underscore too
        json_dict = self._replace_dict_key(
            json_dict, 'id', 'id_', recursion=True)

        if 'port' in json_dict:
            subnet_dict = json_dict.get('port')
            ret = PortResponse(**subnet_dict)
        elif 'ports' in json_dict:
            ret = []
            ports = json_dict.get('ports')
            for port in ports:
                ret.append(PortResponse(**port))
        return ret
