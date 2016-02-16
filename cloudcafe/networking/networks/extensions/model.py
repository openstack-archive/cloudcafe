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

from cafe.engine.models.base \
    import AutoMarshallingListModel, AutoMarshallingModel


class NeutronExtension(AutoMarshallingModel):
    def __init__(self, updated, name, links, namespace, alias, description):
        super(NeutronExtension, self).__init__()
        self.updated = updated
        self.name = name
        self.links = links
        self.namespace = namespace
        self.alias = alias
        self.description = description

    @classmethod
    def _json_to_obj(cls, serialized_str):
        # NOTE: The individual extension summaries do not have a ROOT TAG.
        json_dict = json.loads(serialized_str)
        return cls(**json_dict)


class NeutronExtensions(AutoMarshallingListModel):
    ROOT_TAG = 'extensions'
    LIST_MODEL = NeutronExtension

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)

        extensions = cls()
        for extension in json_dict.get(cls.ROOT_TAG, {}):
            extensions.append(cls.LIST_MODEL(**extension))
        return extensions
