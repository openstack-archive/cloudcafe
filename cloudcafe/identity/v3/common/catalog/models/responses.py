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

import json

from cloudcafe.identity.common.models.base import BaseIdentityModel


class Catalog(BaseIdentityModel):
    """
    Response model for Catalog
    """

    ROOT_TAG = 'catalog'

    def __init__(self, catalog=None, links=None):
        super(Catalog, self).__init__(locals())
        self.catalog = catalog
        self.links = links

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """
        @summary: Converting JSON Representation of Catalog object
            to Catalog object
        @return: Catalog object
        @param serialized_str: JSON Representation of Catalog object
        """
        json_dict = json.loads(serialized_str)
        return cls(Catalog._dict_to_obj(json_dict.get("catalog")),
                   Links._dict_to_obj(json_dict.get("links")))

    @classmethod
    def _dict_to_obj(cls, data):
        """
        @summary: Converting Dictionary Representation of Catalog object
            to Catalog object
        @return: Catalog object
        @param data: Dictionary Representation of Catalog object
        """
        return [Service._dict_to_obj(service) for service in data]


class Links(BaseIdentityModel):
    """
    Response model for links
    """

    def __init__(self, self_=None):
        super(Links, self).__init__(locals())
        self.self_ = self_

    @classmethod
    def _dict_to_obj(cls, data):
        """
        @summary: Converting Dictionary Representation of Links object
            to Links object
        @return: Links object
        @param data: Dictionary Representation of Links object
        """
        return Links(self_=data.get("self"))


class Service(BaseIdentityModel):
    """
    Response model for Service
    """

    def __init__(self, endpoints=None, type=None):
        super(Service, self).__init__(locals())
        self.endpoints = endpoints
        self.type = type

    @classmethod
    def _dict_to_obj(cls, data):
        """
        @summary: Converting Dictionary Representation of Service object
            to Service object
        @return: Service object
        @param data: Dictionary Representation of Service object
        """
        if 'type' in data:
            type = data.get("type")

        if Endpoints.ROOT_TAG in data:
            data[Endpoints.ROOT_TAG] = Endpoints._list_to_obj(
                data[Endpoints.ROOT_TAG]).endpoints
        return Service(**data)


class Endpoints(BaseIdentityModel):
    """
    Response model for Endpoints
    """

    ROOT_TAG = 'endpoints'

    def __init__(self, endpoints=None):
        super(Endpoints, self).__init__(locals())
        self.endpoints = endpoints

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """
        @summary: Converting JSON Representation of Endpoints object
            to Endpoints object
        @return: Endpoints object
        @param serialized_str: JSON Representation of Endpoints object
        """
        json_dict = json.loads(serialized_str)
        return cls._list_to_obj(json_dict.get(cls.ROOT_TAG))

    @classmethod
    def _list_to_obj(cls, list_):
        """
        @summary: Converting List Representation of Endpoints object
            to Endpoints object
        @return: Endpoints object
        @param list_: List Representation of Endpoints object
        """
        ret = {cls.ROOT_TAG: [Endpoint._dict_to_obj(endpoint)
                              for endpoint in list_]}

        return Endpoints(**ret)


class Endpoint(BaseIdentityModel):
    """
    Response model for Endpoint
    """

    def __init__(self, interface=None, region=None, id=None, url=None):
        super(Endpoint, self).__init__(locals())
        self.interface = interface
        self.region = region
        self.id = id
        self.url = url

    @classmethod
    def _dict_to_obj(cls, data):
        """
        @summary: Converting Dictionary Representation of Endpoint object
            to Endpoint object
        @return: Endpoint object
        @param data: Dictionary Representation of Endpoint object
        """
        return Endpoint(id=data.get("id"),
                        region=data.get("region"),
                        url=data.get("url"),
                        interface=data.get("interface"))
