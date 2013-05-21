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

import json
from cloudcafe.identity.v2_0.base import \
    BaseIdentityModel, BaseIdentityListModel


class Extensions(BaseIdentityModel):
    def __init__(self, values=None):
        """
        Models a extensions object returned by keystone
        """
        self.values = values

    @classmethod
    def _dict_to_obj(cls, json_dict):
        extensions = Extensions()
        extensions.values = Values._list_to_obj(
            json_dict.get('extensions'))

        return extensions

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._dict_to_obj(json_dict.get('extensions'))


class Values(BaseIdentityListModel):
    def __init__(self, values=None):
        """
        Models a list of values returned by keystone
        @param values:
        """
        super(Values, self).__init__()
        self.extend(values)

    @classmethod
    def _list_to_obj(self, value_dict_list):
        values = Values([])
        for value_dict in value_dict_list:
            value = Value._dict_to_obj(value_dict)
            values.append(value)

        return values


class Value(BaseIdentityModel):
    def __init__(self, updated=None, name=None, links=None, namespace=None,
                 alias=None, description=None):
        """
        Models a value object returned by keystone
        """
        self.updated = updated
        self.name = name
        self.links = links
        self.namespace = namespace
        self.alias = alias
        self.description = description

    @classmethod
    def _dict_to_obj(cls, json_dict):
        value = Value(updated=json_dict.get('updated'),
                      name=json_dict.get('name'),
                      namespace=json_dict.get('namespace'),
                      alias=json_dict.get('alias'),
                      description=json_dict.get('description'),
                      links=(Links._list_to_obj(json_dict.get('links'))))

        return value


class Links(BaseIdentityListModel):
    def __init__(self, links=None):
        """
        Models a list of links returned by keystone
        """
        super(Links, self).__init__()
        self.extend(links)

    @classmethod
    def _list_to_obj(self, link_dict_list):
        links = Links([])
        for link_dict in link_dict_list:
            link = Link._dict_to_obj(link_dict)
            links.append(link)

        return links


# noinspection PyMissingConstructor
class Link(BaseIdentityModel):
    def __init__(self, href=None, type_=None, rel=None):
        """
        Models a link object returned by keystone
        @param href:
        @param type_:
        @param rel:
        """
        self.href = href
        self.type_ = type_
        self.rel = rel

    @classmethod
    def _dict_to_obj(cls, json_dict):
        link = Link(href=json_dict.get('href'),
                    type_=json_dict.get('type'),
                    rel=json_dict.get('rel'))

        return link