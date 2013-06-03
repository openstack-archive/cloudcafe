import pytest
import re
import os
import requests
from unittest import TestCase
from httpretty import HTTPretty

from cloudcafe.images.v2_0.client import ImageClient
from cloudcafe.images.v2_0.models.image import Image

GLANCE_API_SERVER_ENDPOINT = 'localhost/v2'

class InvalidRequestHeaders(Exception):
    pass

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
                    raise InvalidRequestHeader('Invalid request headers')

            self.response_headers.update({'server': 'Sett\'s Server'})
            
            return self.response_code, self.response_headers, self.response_body

        HTTPretty.register_uri(self.valid_request_method, re.compile(uri), body=callback_response)


class TestImageClient(TestCase):

    @classmethod
    def setup_class(cls):
        cls.raw_image_str = open(os.path.join(
            os.path.dirname(__file__), 'data/image.json')).read()
        cls.raw_images_str = open(os.path.join(
            os.path.dirname(__file__), 'data/images.json')).read()

        cls.raw_images_schema_str = open(os.path.join(
            os.path.dirname(__file__), 'data/images_schema.json')).read()

        if os.environ['MOCK'] == 'True':
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
        image_id_regex = '([0-9a-fA-F]){8}-([0-9a-fA-F]){4}-([0-9a-fA-F]){4}-([0-9a-fA-F]){4}-([0-9a-fA-F]){12}'
        tag_regex = '[\w\d]*'
    
        endpoints = {
            '/schemas/images/?': MockEndpoint(HTTPretty.GET, response_body=cls.raw_images_schema_str),
            '/schemas/image/?': MockEndpoint(HTTPretty.GET, response_headers={}, response_body={}),
            '/images/?': MockEndpoint(HTTPretty.POST, response_headers={}, response_body={}),
            '/images/{0}'.format(image_id_regex):
             MockEndpoint(HTTPretty.PATCH, response_headers={}, response_body={}),
            '/images/{image_id}/tags/{tag}'.format(image_id=image_id_regex, tag=tag_regex): MockEndpoint(HTTPretty.PUT),
            '/images/{image_id}/tags/{tag}'.format(image_id=image_id_regex, tag=tag_regex): MockEndpoint(HTTPretty.DELETE),
            '/images/?': MockEndpoint(HTTPretty.GET, response_body=cls.raw_images_str),
            '/images/{image_id}'.format(image_id=image_id_regex): MockEndpoint(HTTPretty.GET, response_body=cls.raw_image_str)
    
        }  # a list of uri and methods for which the requests must be validated
    
        # register the endpoints
        for uri, endpoint in endpoints.items():
            endpoint.register('{0}{1}'.format(GLANCE_API_SERVER_ENDPOINT, uri))

    @classmethod
    def teardown_class(cls):
        HTTPretty.disable()

    def test_stuff(self):
        HTTPretty.register_uri(HTTPretty.GET, re.compile('localhost/stuff/?'), body='stuff')

        response = requests.get('http://localhost:9292/stuff') 
        assert response.text == 'stuff'
    
    def test_get_image(self):
        response = self.images_client.get_image(self.image_obj.id_)

        print response.content
        assert response is not None

    def test_get_images_schema(self):
        response = self.images_client.get_images_schema()
        
        assert response is not None
        assert response.content == 'stuff'
        print response.content
        assert 0
        
