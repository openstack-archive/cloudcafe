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


class IPAssociation(AutoMarshallingModel):
    """
    @summary: IP Association model response object for the Shared IPs Rackspace
        Compute v2.0 API extension.
    @param id_: Server instance shared IP address ID
    @type id_: str
    @param address: IPv4 or IPv6 shared IP address
    @type address: str
    """

    IP_ASSOCIATION = 'ip_association'

    def __init__(self, id_=None, address=None, **kwargs):

        # kwargs to be used for checking unexpected response attrs
        super(IPAssociation, self).__init__()
        self.id = id_
        self.address = address

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """
        @summary: Return IP association object from a JSON serialized string
        """

        ret = None
        json_dict = json.loads(serialized_str)

        # Replacing attribute response names if they are Python reserved words
        # with a trailing underscore, for ex. id for id_
        json_dict = cls._replace_dict_key(
            json_dict, 'id', 'id_', recursion=True)

        if cls.IP_ASSOCIATION in json_dict:
            ip_address_dict = json_dict.get(cls.IP_ASSOCIATION)
            ret = IPAssociation(**ip_address_dict)
        return ret


class IPAssociations(AutoMarshallingListModel):

    IP_ASSOCIATIONS = 'ip_associations'

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """
        @summary: Return a list of IP association objects from a JSON
            serialized string
        """
        ret = cls()
        json_dict = json.loads(serialized_str)

        # Replacing attribute response names if they are Python reserved words
        # with a trailing underscore, for ex. id for id_
        json_dict = cls._replace_dict_key(
            json_dict, 'id', 'id_', recursion=True)

        if cls.IP_ASSOCIATIONS in json_dict:
            ip_associations = json_dict.get(cls.IP_ASSOCIATIONS)
            for ip_association in ip_associations:
                result = IPAssociation(**ip_association)
                ret.append(result)
        return ret
