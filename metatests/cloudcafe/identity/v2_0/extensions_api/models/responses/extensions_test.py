from unittest import TestCase
from cloudcafe.identity.v2_0.extensions_api.models.responses.extensions \
    import Extensions, Value, Values, Link, Links


class ExtensionsTest(TestCase):
    def setUp(self):
        self.href = "URL"
        self.type = "TEXT_HTML"
        self.rel = "DESCRIBED_BY"
        self.updated_date = "UPDATED_DATE"
        self.name = "KEYSTONE_ADMIN_NAME"

        self.dict_for_link = {"href": self.href, "type": self.type,
                              "rel": self.rel}
        self.name_space = "NAME_SPACE"
        self.alias = "ALIAS"
        self.description = "DESCRIPTION"
        self.dict_for_value = {
            'updated': "UPDATED_DATE",
            'name': "KEYSTONE_ADMIN_NAME",
            'links': [{"href": "URL",
                       "type": "TEXT_HTML",
                       "rel": "DESCRIBED_BY"}],
            'namespace': "NAME_SPACE",
            'alias': "ALIAS",
            'description': "DESCRIPTION"}

        self.link = Link(href=self.href, type_=self.type, rel=self.rel)
        self.links = Links(links=[self.link])

        self.link_dict_list = [self.dict_for_link]
        self.value_dict_list = [self.dict_for_value]

        self.value = Value(updated=self.updated_date,
                           name=self.name,
                           links=[self.link],
                           namespace=self.name_space,
                           alias=self.alias,
                           description=self.description)

        self.values_list = Values(values=[self.value])

        self.extensions = Extensions(values=self.values_list)
        self.dict_for_extensions = {'extensions': [self.dict_for_value]}

    def test_dict_to_obj(self):
        assert self.extensions == Extensions._dict_to_obj(
            self.dict_for_extensions)
        assert self.link == Link._dict_to_obj(self.dict_for_link)
        assert self.value == Value._dict_to_obj(self.dict_for_value)

    def test_list_to_obj(self):
        assert Links._list_to_obj(self.link_dict_list) == self.links
        assert Values._list_to_obj(self.value_dict_list) == self.values_list
