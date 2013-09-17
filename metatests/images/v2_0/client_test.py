import re
import os
from copy import deepcopy
from httpretty import HTTPretty

from cloudcafe.images.v2.client import ImageClient
from cloudcafe.images.v2.models.image import Image

GLANCE_API_SERVER_ENDPOINT = 'localhost/v2'
IS_MOCK = bool(os.environ['MOCK']) or None


class TestImageClient(object):
    image_id_regex = '([0-9a-fA-F]){8}-([0-9a-fA-F]){4}-([0-9a-fA-F]){4}-' \
                     '([0-9a-fA-F]){4}-([0-9a-fA-F]){12}'
    member_id_regex = '[\w\d-]+'
    tag_regex = '[\w\d]*'

    @classmethod
    def setup_class(cls):
        cls.raw_image_str = open(os.path.join(
            os.path.dirname(__file__), 'data/image.json')).read()
        cls.raw_images_str = open(os.path.join(
            os.path.dirname(__file__), 'data/images.json')).read()

        cls.raw_images_schema_str = open(os.path.join(
            os.path.dirname(__file__), 'data/images_schema.json')).read()
        cls.raw_image_schema_str = open(os.path.join(
            os.path.dirname(__file__), 'data/image_schema.json')).read()

        if IS_MOCK:
            HTTPretty.enable()
            cls.mock_api()

        cls.image_obj = Image._json_to_obj(cls.raw_image_str)
        cls.images_obj = Image._json_to_obj(cls.raw_images_str)

        cls.images_client = ImageClient(
            base_url='http://localhost/v2',
            auth_token='36a04b4e71484ab9aacb1d0ac95733fc',
            serialize_format='json',
            deserialize_format='json'
        )

    @classmethod
    def mock_api(cls):
        """
            Set up the URI mapping
        """
        # this is not going to work because some URL
        endpoints = {}

        endpoints['/schemas/images/?$'] = [
            MockEndpoint(HTTPretty.GET,
                         response_body=cls.raw_images_schema_str)
        ]

        endpoints['/schemas/image/?$'] = [
            MockEndpoint(HTTPretty.GET,
                         response_body=cls.raw_image_schema_str)
        ]

        endpoints['/images/?$'] = [
            MockEndpoint(
                HTTPretty.POST,
                response_headers={
                    'Location': (
                        '/v2/images/21c697d1-2cc5-4a45-ba50-61fab15ab9b7')
                },
                response_body=cls.raw_image_str,
                response_code=201),
            MockEndpoint(HTTPretty.GET,
                         response_body=cls.raw_images_str,
                         response_code=200)
        ]

        endpoints['/images/{image_id}$'.format(image_id=cls.image_id_regex)] \
            = [MockEndpoint(
                HTTPretty.PATCH,  # TODO: validate request maybe
                response_body=cls.raw_image_str,
                response_code=201),
               MockEndpoint(
                   HTTPretty.GET,
                   response_body=cls.raw_image_str),
               MockEndpoint(
                   HTTPretty.DELETE,
                   response_code=204)]

        url = '/images/{image_id}/tags/{tag}'.format(
            image_id=cls.image_id_regex,
            tag=cls.tag_regex)
        endpoints[url] = [
            MockEndpoint(HTTPretty.PUT, response_code=204),
            MockEndpoint(HTTPretty.DELETE,
                         responses=[HTTPretty.Response('successfully deleted',
                                                       status=204),
                                    HTTPretty.Response('already deleted',
                                                       status=404)])
        ]

        url = '/images/{image_id}/members'.format(
            image_id=cls.image_id_regex)

        endpoints[url] = [
            MockEndpoint(HTTPretty.GET, response_code=200),
            MockEndpoint(HTTPretty.POST, response_code=200)
        ]

        url = '/images/{image_id}/members/{member_id}$'.format(
            image_id=cls.image_id_regex,
            member_id=cls.member_id_regex)

        endpoints[url] = [
            MockEndpoint(HTTPretty.DELETE, response_code=204),
            MockEndpoint(HTTPretty.PUT, response_code=200)
        ]

        # register the endpoints
        for uri, responses in endpoints.items():
            for response in responses:
                response.register('{0}{1}'.format(
                    GLANCE_API_SERVER_ENDPOINT, uri))

    @classmethod
    def teardown_class(cls):
        HTTPretty.disable()

    def test_get_images_schema(self):
        response = self.images_client.get_images_schema()

        assert response is not None
        if IS_MOCK:
            assert response.content == self.raw_images_schema_str

    def test_get_image_schema(self):
        response = self.images_client.get_image_schema()

        assert response is not None
        if IS_MOCK:
            assert self.raw_image_schema_str

    def test_create_image(self):
        new_image = deepcopy(self.image_obj)

        #response = self.images_client.create_image(**new_image.__dict__)
        response = self.images_client.create_image(
            id_=new_image.id_, name=new_image.name,
            visibility=new_image.visibility, status=new_image.status,
            protected=new_image.protected, tags=new_image.tags,
            checksum=new_image.checksum, size=new_image.size,
            created_at=new_image.created_at, updated_at=new_image.updated_at,
            file_=new_image.file_, self_=new_image.self_,
            schema=new_image.schema,
            container_format=new_image.container_format,
            disk_format=new_image.disk_format, min_disk=new_image.min_disk,
            min_ram=new_image.min_ram, kernel_id=new_image.kernel_id,
            ramdisk_id=new_image.ramdisk_id)

        valid_uri = re.compile('/v2/images/{0}'.format(self.image_id_regex))
        assert response is not None
        assert 201 == response.status_code
        assert re.match(valid_uri, response.headers.get('location'))

    def test_update_image(self):
        image_id = self.image_obj.id_
        new_properties = {'name': 'ciross-0.3.1',
                          'new_prop': 'new_value'}

        response = self.images_client.update_image(
            image_id,
            new_properties
        )

        assert response is not None
        assert 201 == response.status_code
        assert self.raw_image_str == response.content

    def test_add_image_tag(self):
        image_id = self.image_obj.id_
        new_tag = 'miracle'

        response = self.images_client.add_tag(image_id, new_tag)

        assert response is not None
        assert 204 == response.status_code

    def test_delete_image_tag(self):
        image_id = self.image_obj.id_
        tag = 'miracle'

        response = self.images_client.delete_tag(image_id, tag)

        assert response is not None
        assert 204 == response.status_code

        response = self.images_client.delete_tag(image_id, tag)

        assert response is not None
        assert 404 == response.status_code

    def test_list_images(self):
        response = self.images_client.list_images()

        assert 200 == response.status_code
        assert self.raw_images_str == response.content

    def test_get_image(self):
        image_id = self.image_obj.id_

        response = self.images_client.get_image(image_id)

        assert response is not None
        assert 200 == response.status_code
        assert self.raw_image_str == response.content

    def test_delete_image(self):
        image_id = self.image_obj.id_

        response = self.images_client.delete_image(image_id)

        assert response is not None
        assert 204 == response.status_code

    def test_list_members_from_image(self):
        image_id = self.image_obj.id_

        response = self.images_client.list_members(image_id)
        assert response is not None
        assert 200 == response.status_code

    def test_add_member_to_image(self):
        image_id = self.image_obj.id_

        response = self.images_client.add_member(image_id, 'someguy')
        assert response is not None
        assert 200 == response.status_code

    def test_delete_member_from_image(self):
        image_id = self.image_obj.id_

        response = self.images_client.delete_member(image_id, 'someguy')
        assert response is not None
        assert 204 == response.status_code

    def test_update_member_of_image(self):
        image_id = self.image_obj.id_

        response = self.images_client.update_member(image_id, 'someguy',
                                                    'accepted')
        assert response is not None
        assert 200 == response.status_code


class MockEndpoint:
    def __init__(self, request_method, request_headers={}, request_body='',
                 response_code=200, response_headers={}, response_body='',
                 responses=None):
        self.valid_request_headers = request_headers
        self.valid_request_method = request_method
        self.valid_request_body = request_body
        self.response_code = response_code
        self.response_headers = response_headers
        self.response_body = response_body
        self.responses = responses

    def register(self, uri):
        def callback_response(method, uri, headers):
            """

            @param method:
            @param uri:
            @param headers:
            @return: @raise:
            """
            for key, val in self.valid_request_headers.items():
                if headers.get(key) != val:
                    raise AssertionError(key, val, headers.get(key))

            self.response_headers.update({'server': 'HTTPretty Mock Server'})

            return (self.response_code, self.response_headers,
                    self.response_body)

        if self.responses:
            HTTPretty.register_uri(self.valid_request_method, re.compile(uri),
                                   headers=self.response_headers,
                                   responses=self.responses)
        else:
            HTTPretty.register_uri(self.valid_request_method, re.compile(uri),
                                   headers=self.response_headers,
                                   body=callback_response)


class InvalidRequestHeaderError(AssertionError):
    def __init__(self, expected_key, expected_value, actual_value):
        super(InvalidRequestHeaderError, self).__init__()
        self.message = '''Invalid request header. \n
            Expected ({0}: {1})\n
            Received ({0}: {2})''' \
            .format(expected_key, expected_value, actual_value)
