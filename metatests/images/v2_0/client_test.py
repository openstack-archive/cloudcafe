import re
import os
from copy import deepcopy
from unittest import TestCase
from httpretty import HTTPretty

from cloudcafe.images.v2_0.client import ImageClient
from cloudcafe.images.v2_0.models.image import Image

GLANCE_API_SERVER_ENDPOINT = 'localhost/v2'
IS_MOCK = bool(os.environ['MOCK']) or None


class TestImageClient(TestCase):
    image_id_regex = '([0-9a-fA-F]){8}-([0-9a-fA-F]){4}-([0-9a-fA-F]){4}-([0-9a-fA-F]){4}-([0-9a-fA-F]){12}'
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
            base_url='http://localhost:9292/v2',
            auth_token='36a04b4e71484ab9aacb1d0ac95733fc',
            serialize_format='json',
            deserialize_format='json'
        )

    @classmethod
    def mock_api(cls):

        endpoints = {
            '/schemas/images/?': MockEndpoint(
                HTTPretty.GET,
                response_body=cls.raw_images_schema_str),
            '/schemas/image/?': MockEndpoint(
                HTTPretty.GET,
                response_body=cls.raw_image_schema_str),
            '/images': MockEndpoint(
                HTTPretty.POST,
                response_headers={
                    'Location':
                    '/v2/images/21c697d1-2cc5-4a45-ba50-61fab15ab9b7'
                },
                response_body=cls.raw_image_str),
            '/images/{0}'.format(cls.image_id_regex):
            MockEndpoint(
                HTTPretty.PATCH,  # TODO: validate request
                response_body=cls.raw_image_str)
#            '/images/{image_id}/tags/{tag}'.format(image_id=cls.image_id_regex, tag=cls.tag_regex): MockEndpoint(HTTPretty.PUT),
#            '/images/{image_id}/tags/{tag}'.format(image_id=cls.image_id_regex, tag=cls.tag_regex): MockEndpoint(HTTPretty.DELETE),
#            '/images/?': MockEndpoint(HTTPretty.GET, response_body=cls.raw_images_str),
#            '/images/{image_id}'.format(image_id=cls.image_id_regex): MockEndpoint(HTTPretty.GET, response_body=cls.raw_image_str)
#
        }  # a list of uri and methods for which the requests must be validated

        # register the endpoints
        for uri, endpoint in endpoints.items():
            endpoint.register('{0}{1}'.format(GLANCE_API_SERVER_ENDPOINT, uri))

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
            assert response.content == self.raw_image_schema_str

    def test_create_image(self):
        new_image = deepcopy(self.image_obj)
        response = self.images_client.create_image(new_image)

        valid_uri = re.compile('/v2/images/{0}'.format(self.image_id_regex))
        assert response is not None
        print response.headers.get('location')
        assert re.match(valid_uri, response.headers.get('location'))

    def test_update_image(self):
        image_id = self.image_obj.id_
        new_properties = {'name': 'ciross-0.3.1'}

        response = self.images_client.update_image(
            image_id,
            new_properties
        )

        assert response is not None

#    def test_get_image(self):
#        response = self.images_client.get_image(self.image_obj.id_)
#
#        print response.content
#        assert response is not None


class MockEndpoint:
    def __init__(self, request_method, request_headers={}, request_body='',
                 response_code=200, response_headers={}, response_body=''):
        self.valid_request_headers = request_headers
        self.valid_request_method = request_method
        self.valid_request_body = request_body
        self.response_code = response_code
        self.response_headers = response_headers
        self.response_body = response_body

    def register(self, uri):
        def callback_response(method, uri, headers):
            for key, val in self.valid_request_headers.items():
                if headers.get(key) != val:
                    raise Exception('Invalid request headers')

            self.response_headers.update({'server': 'Sett\'s Server'})

            return self.response_code, self.response_headers, \
                self.response_body

        HTTPretty.register_uri(self.valid_request_method, re.compile(uri),
                               headers=self.response_headers,
                               body=callback_response)
