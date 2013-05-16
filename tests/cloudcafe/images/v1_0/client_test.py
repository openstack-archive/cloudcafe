import re
from unittest import TestCase
from cloudcafe.images.v1_0.client import ImagesClient
from httpretty import HTTPretty

GLANCE_API_SERVER_ENDPOINT = 'http://localhost:9292/v1'


class ClientTest(TestCase):

    @classmethod
    def setup_class(cls):
        HTTPretty.enable()

        cls.images_client = ImagesClient(
            url=GLANCE_API_SERVER_ENDPOINT,
            auth_token="36a04b4e71484ab9aacb1d0ac95733fc",
            serialize_format="json",
            deserialize_format="json"
        )

        cls.image_id = '1c675abd94f49cda114e12490b328d9'
        cls.images_uri = GLANCE_API_SERVER_ENDPOINT + '/images/'
        cls.image_uri = cls.images_uri + cls.image_id

    @classmethod
    def teardown_class(cls):
        HTTPretty.disable()

    def setup_method(self, method):
        if method.__name__ is 'test_retrieve_image_metadata' or \
                method.__name__ is 'test_retrieve_raw_image_data' or \
                method.__name__ is 'test_update_image':
            self.expected_headers = {
                'x-image-meta-uri':
                '{0}/images/1c675abd94f49cda114e12490b328d9'
                .format(GLANCE_API_SERVER_ENDPOINT),
                'x-image-meta-name': 'Ubuntu 10.04 Plain 5GB',
                'x-image-meta-disk_format': 'vhd',
                'x-image-meta-container_format': 'ovf',
                'x-image-meta-size': '5368709120',
                'x-image-meta-checksum': 'c2e5db72bd7fd153f53ede5da5a06de3',
                'x-image-meta-created_at': '2010-02-03 09:34:01',
                'x-image-meta-updated_at': '2010-02-03 09:34:01',
                'x-image-meta-deleted_at': '',
                'x-image-meta-status': 'available',
                'x-image-meta-is_public': 'true',
                'x-image-meta-min-ram': '256',
                'x-image-meta-min-disk': '0',
                'x-image-meta-owner': 'null',
                'x-image-meta-property-distro': 'Ubuntu 10.04 LTS'
            }

    def test_list_available_images(self):
        HTTPretty.register_uri(HTTPretty.GET, self.images_uri,
                               body=self._build_response_body(),
                               content_type="application/json")

        actual_response = self.images_client.list_images()

        assert HTTPretty.last_request.headers['X-Auth-Token'] == \
            '36a04b4e71484ab9aacb1d0ac95733fc'
        assert HTTPretty.last_request.headers['Content-Type'] == \
            'application/json'
        assert HTTPretty.last_request.headers['Accept'] == 'application/json'

        assert 200 == actual_response.status_code
        assert self._build_response_body() == actual_response.content
        assert self.images_uri == actual_response.url
        assert self._build_response_body() == actual_response.content
        assert self.images_uri == actual_response.url

    def test_get_image(self):
        HTTPretty.register_uri(HTTPretty.GET, self.image_uri,
                               body=self._build_response_body(),
                               content_type="application/json")

        actual_response = self.images_client.get_image(image_id=self.image_id)

        assert HTTPretty.last_request.headers['X-Auth-Token'] == \
            '36a04b4e71484ab9aacb1d0ac95733fc'
        assert HTTPretty.last_request.headers['Content-Type'] == \
            'application/json'
        assert HTTPretty.last_request.headers['Accept'] == 'application/json'

        assert 200 == actual_response.status_code
        assert self._build_response_body() == actual_response.content
        assert self.image_uri == actual_response.url

    def test_filter_images_list(self):
        filtering_parameters = {'name': 'precise', 'status': 'active',
                                'container_format': 'bare',
                                'disk_format': 'qcow2',
                                'min_disk': '0', 'size': '252116992'}
        HTTPretty.register_uri(
            HTTPretty.GET,
            "{0}/images?status=active&name=precise&container_format=bare&\
                    disk_format=qcow2&min_disk=0&size=252116992"
            .format(GLANCE_API_SERVER_ENDPOINT),
            body=self._build_response_body(),
            content_type="application/json")

        actual_response = self.images_client.filter_images_list(
            filtering_parameters)
        request_querystring = HTTPretty.last_request.querystring
        expected_request_querystring = self._get_querystring_data(
            request_querystring)

        assert expected_request_querystring == filtering_parameters
        assert HTTPretty.last_request.headers['X-Auth-Token'] == \
            '36a04b4e71484ab9aacb1d0ac95733fc'
        assert HTTPretty.last_request.headers['Content-Type'] == \
            'application/json'
        assert HTTPretty.last_request.headers['Accept'] == 'application/json'

        assert 200 == actual_response.status_code
        assert self._build_response_body() == actual_response.content

    def test_add_image(self):
        HTTPretty.register_uri(HTTPretty.POST, self.images_uri,
                               body='Adding New Image',
                               adding_headers={'x-image-meta-property-distro':
                                               'Ubuntu 10.04 LTS'})

        image_name = 'Ubuntu 10.04 Plain 5GB'
        actual_response = self.images_client.add_image(image_name=image_name,
                                                       image_data=None)

        assert 'x-image-meta-name' in \
            HTTPretty.last_request.headers.keys()

        assert 200 == actual_response.status_code
        assert self.images_uri == actual_response.url
        assert 'Adding New Image' == actual_response.content
        assert 'x-image-meta-property-distro' in \
            actual_response.__dict__['headers'].keys()

    def test_retrieve_image_metadata(self):
        url = self.images_uri + '71c675ab-d94f-49cd-a114-e12490b328d9'
        HTTPretty.register_uri(HTTPretty.HEAD, url, body='Raw Image Data',
                               headers=self.expected_headers)

        actual_response = self.images_client.retrieve_metadata(
            '71c675ab-d94f-49cd-a114-e12490b328d9'
        )
        uri_regex = re.compile(
            '{0}[\w\d]{{8}}-[\w\d]{{4}}-[\w\d]{{4}}-[\w\d]{{4}}-[\w\d]{{12}}'
            .format(self.images_uri)
        )
        assert re.match(uri_regex, actual_response.url) is not None
        assert HTTPretty.last_request.headers['X-Auth-Token'] == \
            '36a04b4e71484ab9aacb1d0ac95733fc'
        assert HTTPretty.last_request.headers['Content-Type'] == \
            'application/json'
        assert HTTPretty.last_request.headers['Accept'] == 'application/json'
        assert 200 == actual_response.status_code

    def test_retrieve_raw_image_data(self):
        url = self.images_uri + '71c675ab-d94f-49cd-a114-e12490b328d9'
        HTTPretty.register_uri(HTTPretty.GET, url, body='Raw Image Data',
                               headers=self.expected_headers)

        actual_response = self.images_client.retrieve_raw_image_data(
            '71c675ab-d94f-49cd-a114-e12490b328d9'
        )
        uri_regex = re.compile(
            '{0}[\w\d]{{8}}-[\w\d]{{4}}-[\w\d]{{4}}-[\w\d]{{4}}-[\w\d]{{12}}'
            .format(self.images_uri)
        )
        assert re.match(uri_regex, actual_response.url) is not None
        assert HTTPretty.last_request.headers['X-Auth-Token'] == \
            '36a04b4e71484ab9aacb1d0ac95733fc'
        assert HTTPretty.last_request.headers['Content-Type'] == \
            'application/json'
        assert HTTPretty.last_request.headers['Accept'] == 'application/json'
        assert 200 == actual_response.status_code

    def test_list_image_memberships(self):
        url = self.image_uri + '/members'
        HTTPretty.register_uri(HTTPretty.GET,
                               url, body=self._build_list_image_membership())

        actual_response = \
            self.images_client.list_image_membership(self.image_id)

        assert 200 == actual_response.status_code
        assert url == actual_response.url

    def _build_response_body(self):
        return '{"images": '\
               '[{"status": "active", '\
               '"name": "precise", '\
               '"deleted": false, '\
               '"container_format": "bare", '\
               '"created_at": "2013-04-29T19:32:56", '\
               '"disk_format": "qcow2", '\
               '"updated_at": "2013-04-29T19:32:56", '\
               '"properties": {}, '\
               '"min_disk": 0, '\
               '"protected": false, '\
               '"id": "46fd5b5c-b925-4316-a878-63cbbe7f0030", '\
               '"checksum": null, '\
               '"owner": "bd7531a57d3a47538fae1b89c169b293", '\
               '"is_public": true, '\
               '"deleted_at": null, '\
               '"min_ram": "0", '\
               '"size": "252116992"}]}'

    def _get_querystring_data(self, querystring):
        querystring_data = {}
        for key in querystring:
            querystring_data[key] = querystring[key][0] or \
                int(querystring[key][0])

        return querystring_data

    def _build_list_image_membership(self):
        """@summary: Get the members_list attribute (image.members_list)
        for an image with id=image_id"""

        return {'members': 'members_list'}

    def test_update_image(self):
        url = self.images_uri + '71c675ab-d94f-49cd-a114-e12490b328d9'
        HTTPretty.register_uri(HTTPretty.PUT, url, body='Updated Image',
                               headers=self.expected_headers)

        actual_response = self.images_client.update_image(
            '71c675ab-d94f-49cd-a114-e12490b328d9',
            image_meta_is_public=False)

        uri_regex = re.compile(
            '{0}[\w\d]{{8}}-[\w\d]{{4}}-[\w\d]{{4}}-[\w\d]{{4}}-[\w\d]{{12}}'
            .format(self.images_uri)
        )
        assert re.match(uri_regex, actual_response.url) is not None
        assert HTTPretty.last_request.headers['X-Auth-Token'] == \
            '36a04b4e71484ab9aacb1d0ac95733fc'
        assert 200 == actual_response.status_code

    def test_list_shared_images(self):
        member_id = ''
        shared_images_url = '{0}/shared-images/{1}'.format(
            GLANCE_API_SERVER_ENDPOINT,
            member_id
        )

        HTTPretty.register_uri(HTTPretty.GET, shared_images_url,
                               body=self._build_list_shared_images())

        actual_response = self.images_client.list_shared_images(member_id)

        assert 200 == actual_response.status_code
        assert shared_images_url == actual_response.url

    def _build_list_shared_images(self):
        """@summary: Get the shared_images attribute (member.shared_attributes)
        for a member with id=member_id"""

        return {'shared_images': 'shared_images'}

    def test_add_member_to_an_image(self):
        member_id = ''
        url = self.image_uri + '/members/' + member_id
        HTTPretty.register_uri(HTTPretty.PUT, url, body={})

        actual_response = self.images_client.add_member_to_image(self.image_id,
                                                                 member_id)

        assert 200 == actual_response.status_code
        assert url == actual_response.url

    def test_remove_member_from_an_image(self):
        member_id = ''
        url = self.image_uri + '/members/' + member_id
        HTTPretty.register_uri(HTTPretty.DELETE, url, body={})

        actual_response = \
            self.images_client.delete_member_from_image(self.image_id,
                                                        member_id)

        assert 200 == actual_response.status_code
        assert url == actual_response.url

    def test_replace_members_list_for_an_image(self):
        url = self.image_uri + '/members/'
        HTTPretty.register_uri(HTTPretty.PUT, url,
                               body=self._build_members_list())

        actual_response = \
            self.images_client.replace_members_list(self.image_id)

        assert 200 == actual_response.status_code
        assert url == actual_response.url

    def _build_members_list(self):
        return {'memberships': 'new_members_list'}
