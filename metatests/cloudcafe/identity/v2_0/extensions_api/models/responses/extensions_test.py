from unittest import TestCase
from cloudcafe.identity.v2_0.extensions_api.models.responses.extensions import \
    Extensions, Value, Values, Link, Links


class ExtensionsTest(TestCase):
    def setUp(self):
        self.href = "URL (e.g.:https://github.com/openstack/identity-api)"
        self.type = "TEXT_HTML (e.g.:text/html)"
        self.rel = "DESCRIBED_BY (e.g.: described by)"
        self.updated_date = "UPDATED_DATE (e.g.:2011-08-19T13:25:27-06:00)"
        self.name = "KEYSTONE_ADMIN_NAME (E.G.: Openstack Keystone Admin)"

        self.dict_for_link = {"href": self.href, "type": self.type, "rel": self.rel}
        self.name_space = "NAME_SPACE(e.g.: http://docs.openstack.org/identity/api/ext/OS-KSADM/v1.0)"
        self.alias = "ALIAS (e.g.: OS-KSADM)"
        self.description = "DESCRIPTION (e.g.: Openstack extensions to Keystone v2.0 API enabling Admin Operations.)"
        self.dict_for_value = {
            'updated': "UPDATED_DATE (e.g.:2011-08-19T13:25:27-06:00)",
            'name': "KEYSTONE_ADMIN_NAME (E.G.: Openstack Keystone Admin)",
            'links': [{"href": "URL (e.g.:https://github.com/openstack/identity-api)",
                       "type": "TEXT_HTML (e.g.:text/html)",
                       "rel": "DESCRIBED_BY (e.g.: described by)"}],
            'namespace': "NAME_SPACE(e.g.: http://docs.openstack.org/identity/api/ext/OS-KSADM/v1.0)",
            'alias': "ALIAS (e.g.: OS-KSADM)",
            'description': "DESCRIPTION (e.g.: Openstack extensions to Keystone v2.0 API enabling Admin Operations.)"
        }

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
        assert Extensions._dict_to_obj(self.dict_for_extensions) == self.extensions
        assert Link._dict_to_obj(self.dict_for_link) == self.link
        assert Value._dict_to_obj(self.dict_for_value) == self.value

    def test_list_to_obj(self):
        assert Links._list_to_obj(self.link_dict_list) == self.links
        assert Values._list_to_obj(self.value_dict_list) == self.values_list
