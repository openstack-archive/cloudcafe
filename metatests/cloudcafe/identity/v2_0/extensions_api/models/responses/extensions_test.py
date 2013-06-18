import json
from unittest import TestCase
import os
from cloudcafe.identity.v2_0.extensions_api.models.responses.extensions \
    import Extensions, Value, Values, Link, Links


class ExtensionsTest(TestCase):
    def setUp(self):
        self.extensions_json_dict = \
            open(os.path.join(os.path.dirname(__file__),
                              "../../data/extensions.json")).read()
        self.extensions_dict = json.loads(self.extensions_json_dict).get(
            'extensions')
        self.values = self.extensions_dict.get('values')
        self.links = self.values[0].get('links')
        self.dict_for_link = self.links[0]
        self.href = self.dict_for_link.get('href')
        self.type = self.dict_for_link.get('type')
        self.rel = self.dict_for_link.get('rel')

        self.updated_date = self.values[0].get('updated')
        self.name = self.values[0].get('name')
        self.name_space = self.values[0].get('namespace')
        self.alias = self.values[0].get('alias')
        self.description = self.values[0].get('description')

        self.expected_link = Link(href=self.href, type_=self.type, rel=self.rel)
        self.expected_links = Links(links=[self.expected_link])

        self.expected_value = Value(updated=self.updated_date,
                           name=self.name,
                           links=[self.expected_link],
                           namespace=self.name_space,
                           alias=self.alias,
                           description=self.description)
        self.expected_values = Values(values=[self.expected_value])

        self.expected_extensions = Extensions(values=self.expected_values)
        self.dict_for_extensions = {'extensions': self.values}

    def test_dict_to_obj(self):
        assert self.expected_extensions == Extensions._dict_to_obj(
            self.dict_for_extensions)
        assert self.expected_link == Link._dict_to_obj(self.dict_for_link)
        assert self.expected_value == Value._dict_to_obj(self.values[0])

    def test_list_to_obj(self):
        assert self.expected_values == Values._list_to_obj(self.values)
        assert self.expected_links == Links._list_to_obj(self.links)
