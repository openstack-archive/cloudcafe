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

from cafe.engine.models.base import (
    AutoMarshallingModel, AutoMarshallingListModel)


class Link(AutoMarshallingModel):
    """@summary: Link model"""

    def __init__(self, href=None, rel=None):
        super(Link, self).__init__()
        self.href = href
        self.rel = rel

    @classmethod
    def _dict_to_obj(cls, json_dict):
        link = Link(href=json_dict.get('href'), rel=json_dict.get('rel'))
        return link

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        raise NotImplementedError(
            'Glance does not serve XML-formatted resources')

    def _obj_to_xml(self):
        raise NotImplementedError(
            'Glance does not serve XML-formatted resources')


class Links(AutoMarshallingListModel):
    """@summary: Links model"""

    def __init__(self, links=None):
        self.extend(links or [])

    @classmethod
    def _list_to_obj(cls, link_dict_list):
        links = Links()
        for link_dict in link_dict_list:
            links.append(Link._dict_to_obj(link_dict))
        return links
