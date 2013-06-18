import re

from httpretty import HTTPretty


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
            for key, val in self.valid_request_headers.items():
                if headers.get(key) != val:
                    raise AssertionError(key, val, headers.get(key))

            self.response_headers.update({'server': 'HTTPretty Mock Server'})

            return self.response_code, self.response_headers, \
                self.response_body

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
        super(self).__init__()
        self.message = '''Invalid request header. \n
            Expected ({0}: {1})\n
            Received ({0}: {2})''' \
            .format(expected_key, expected_value, actual_value)
